# src/summarization/core.py

from typing import Optional
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph

llm: Optional[ChatGroq] = None
app: Optional[StateGraph] = None
text_splitter: Optional[RecursiveCharacterTextSplitter] = None