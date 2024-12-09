from typing import Optional
from dataclasses import dataclass
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph


@dataclass
class Core:
    llm: Optional[ChatGroq] = None
    app: Optional[StateGraph] = None
    text_splitter: Optional[RecursiveCharacterTextSplitter] = None
