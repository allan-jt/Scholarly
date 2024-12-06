# src/summarization/summary.py

import asyncio
from langchain_core.documents import Document

# Import the core module to access the initialized variables
import src.summarization.core as core

def summary(input_text: str) -> str:
    """
    Summarizes the given input text by splitting it into chunks,
    processing it through the state graph, and returning the final summary.

    Args:
        input_text (str): The text to summarize.

    Returns:
        str: The final summary of the input text.
    """
    if core.llm is None or core.app is None or core.text_splitter is None:
        raise ValueError("Model is not initialized. Please call `initialize_model()` first.")

    async def process_steps():
        # Split the input text into smaller chunks
        docs = [Document(page_content=input_text)]
        split_docs = core.text_splitter.split_documents(docs)
        print(f"Generated {len(split_docs)} split documents.")

        final_summary = None  # Variable to store the final summary
        steps = core.app.astream(
            {"contents": [doc.page_content for doc in split_docs]},
            {"recursion_limit": 100},
        )
        try:
            async for step in steps:
                if "generate_final_summary" in step:
                    # print("Final Summary:", step["generate_final_summary"])
                    final_summary = step["generate_final_summary"]
                    break  # Gracefully exit the loop
        finally:
            await steps.aclose()  # Explicitly close the generator

        return final_summary

    # Run the asynchronous workflow using the event loop
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(process_steps())
