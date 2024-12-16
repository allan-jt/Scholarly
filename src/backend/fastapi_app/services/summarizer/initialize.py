import os
from langchain_openai import ChatOpenAI

# from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents.reduce import (
    acollapse_docs,
    split_list_of_docs,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langgraph.constants import START, END, Send
from langgraph.graph import StateGraph
from typing import List, Literal, TypedDict, Annotated
import operator

# import yaml

# Import the core module to access and modify global variables
from .core import Core


config = {
    "llm": {
        "model_name": "gpt-4o-mini",
        "temperature": 0,
        "max_token": 500,  # Max number of tokens to generate for each input text
        "max_retries": 2,
    },
    "langraph": {
        "chunk_size": 5000,  # Chunk the input tokens into smaller subdocs if exceeded this number
        "chunk_overlap": 0,
        "summary_token_max": 1000,  # Recursive summarization if summary exceeds this number
        "recursion_limit": 10,  # Max recursion of above step
    },
    "prompt": {
        "map_prompt": (
            "You are an assistant highly skilled at summarizing segments of academic research papers. "
            "I will provide you with one section of the paper at a time. You will not receive the entire paper at once. "
            "Based solely on the segment you are given, please produce a concise and accurate summary of its key points.\n"
            "Your summary should:\n"
            "1. Capture the primary focus of the given section.\n"
            "2. Highlight the key words.\n"
            "3. Clearly describe methodologies and their counterparts if there were any, highlight these and their outcomes.\n"
            "4. Include important quantitative or qualitative data if it appears in the text.\n"
            "5. Exclude any references or citation lists. If the section includes what appears to be a reference section or citation details, ignore them.\n"
            "6. Keep the summaries brief and easy to read in a minute.\n"
            "Summarize the following text:\\n\\n{context}. Output the summary only."
        ),
        "reduce_prompt": (
            "The following is several chunk-level summaries created in isolation from a specific section in a research paper:\n"
            "{docs}. Take these and distill it into a final, consolidated summary of the main themes."
        ),
    },
}


def initialize_model(core: Core):
    """
    Initializes the LLM model, prompt chains, and the state graph.
    This function should be called only once during the application lifecycle.
    """
    if core.llm is not None:
        print("Model is already initialized. Skipping initialization.")
        return

    # Set your GROQ API key securely (replace 'your_api_key_here' with your actual API key)
    # It's recommended to use environment variables or secure storage for API keys

    # with open("./services/summarizer/config.yaml", "r") as f:
    #     config = yaml.safe_load(f)
    model_name = config["llm"]["model_name"]
    temperature = config["llm"]["temperature"]
    max_retries = config["llm"]["max_retries"]
    max_token = config["llm"]["max_token"]
    chunk_size = config["langraph"]["chunk_size"]
    chunk_overlap = config["langraph"]["chunk_overlap"]
    summary_token_max = config["langraph"]["summary_token_max"]
    map_prompt_str = config["prompt"]["map_prompt"]
    reduce_prompt_str = config["prompt"]["reduce_prompt"]

    # Initialize the LLM instance
    # os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    # core.llm = ChatGroq(
    #     model=model_name,
    #     temperature=temperature,
    #     max_tokens=max_token,
    #     timeout=None,
    #     max_retries=max_retries,
    # )
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    core.llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        max_tokens=max_token,
        timeout=None,
        max_retries=max_retries,
    )

    # Define prompt templates and chains for summarization
    map_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                map_prompt_str,
            )
        ]
    )
    map_chain = map_prompt | core.llm | StrOutputParser()

    reduce_template = reduce_prompt_str
    reduce_prompt = ChatPromptTemplate.from_messages([("human", reduce_template)])
    reduce_chain = reduce_prompt | core.llm | StrOutputParser()

    # Initialize a text splitter for chunking input text
    core.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )

    # Define the overall state for the state graph
    class OverallState(TypedDict):
        contents: List[str]
        summaries: Annotated[list, operator.add]
        collapsed_summaries: List[Document]
        final_summary: str

    class SummaryState(TypedDict):
        content: str

    # Define a function to calculate the total number of tokens
    def length_function(documents: List[Document]) -> int:
        return sum(core.llm.get_num_tokens(doc.page_content) for doc in documents)

    # Define the nodes for the state graph
    async def generate_summary(state: SummaryState):
        """
        Asynchronously generates a summary for a given text chunk.
        """
        response = await map_chain.ainvoke(state["content"])
        return {"summaries": [response]}

    def map_summaries(state: OverallState):
        """
        Maps input text chunks to the `generate_summary` function.
        """
        return [
            Send("generate_summary", {"content": content})
            for content in state["contents"]
        ]

    def collect_summaries(state: OverallState):
        """
        Collects summaries and converts them into Document objects.
        """
        return {
            "collapsed_summaries": [Document(summary) for summary in state["summaries"]]
        }

    async def collapse_summaries(state: OverallState):
        """
        Reduces the number of summaries by collapsing them iteratively.
        """
        doc_lists = split_list_of_docs(
            state["collapsed_summaries"], length_function, summary_token_max
        )
        results = []
        for doc_list in doc_lists:
            summaries = await acollapse_docs(doc_list, reduce_chain.ainvoke)
            results.extend(summaries)

        return {
            "collapsed_summaries": [Document(page_content=str(res)) for res in results]
        }

    def should_collapse(
        state: OverallState,
    ) -> Literal["collapse_summaries", "generate_final_summary"]:
        """
        Determines whether further collapsing of summaries is needed.
        """
        num_tokens = length_function(state["collapsed_summaries"])
        if num_tokens > summary_token_max:
            return "collapse_summaries"
        else:
            return "generate_final_summary"

    async def generate_final_summary(state: OverallState):
        """
        Generates the final consolidated summary from all collapsed summaries.
        """
        response = await reduce_chain.ainvoke(state["collapsed_summaries"])
        return {"final_summary": response}

    # Build and compile the state graph
    graph = StateGraph(OverallState)
    graph.add_node("generate_summary", generate_summary)
    graph.add_node("collect_summaries", collect_summaries)
    graph.add_node("collapse_summaries", collapse_summaries)
    graph.add_node("generate_final_summary", generate_final_summary)

    graph.add_conditional_edges(START, map_summaries, ["generate_summary"])
    graph.add_edge("generate_summary", "collect_summaries")
    graph.add_conditional_edges("collect_summaries", should_collapse)
    graph.add_conditional_edges("collapse_summaries", should_collapse)
    graph.add_edge("generate_final_summary", END)

    core.app = graph.compile()
    print("Model and state graph initialized!")

    return core
