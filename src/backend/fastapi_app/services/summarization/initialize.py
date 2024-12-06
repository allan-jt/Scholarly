# src/summarization/initialize.py

import os
from langchain_groq import ChatGroq
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

# Import the core module to access and modify global variables
import src.summarization.core as core

def initialize_model():
    """
    Initializes the LLM model, prompt chains, and the state graph.
    This function should be called only once during the application lifecycle.
    """
    if core.llm is not None:
        print("Model is already initialized. Skipping initialization.")
        return

    # Set your GROQ API key securely (replace 'your_api_key_here' with your actual API key)
    # It's recommended to use environment variables or secure storage for API keys
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "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")

    # Initialize the LLM instance
    core.llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=500,
        timeout=None,
        max_retries=2,
    )

    # Define prompt templates and chains for summarization
    map_prompt = ChatPromptTemplate.from_messages(
        [("system", "Write a concise summary of the following:\n\n{context}")]
    )
    map_chain = map_prompt | core.llm | StrOutputParser()

    reduce_template = """
    The following is a set of summaries:
    {docs}
    Take these and distill it into a final, consolidated summary of the main themes.
    """
    reduce_prompt = ChatPromptTemplate.from_messages([("human", reduce_template)])
    reduce_chain = reduce_prompt | core.llm | StrOutputParser()

    # Initialize a text splitter for chunking input text
    core.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=0, length_function=len
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
            Send("generate_summary", {"content": content}) for content in state["contents"]
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
            state["collapsed_summaries"], length_function, 500
        )
        results = []
        for doc_list in doc_lists:
            summaries = await acollapse_docs(doc_list, reduce_chain.ainvoke)
            results.extend(summaries)

        return {
            "collapsed_summaries": [Document(page_content=str(res)) for res in results]
        }

    def should_collapse(state: OverallState) -> Literal["collapse_summaries", "generate_final_summary"]:
        """
        Determines whether further collapsing of summaries is needed.
        """
        num_tokens = length_function(state["collapsed_summaries"])
        if num_tokens > 500:
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
