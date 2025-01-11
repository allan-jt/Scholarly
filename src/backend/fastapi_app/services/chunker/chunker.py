from services.spark import *
from services.redis import *
from .pdf_parser import *
from io import BytesIO
import fitz


class ChunkerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChunkerSingleton, cls).__new__(cls)
        return cls._instance

    def chunk_pdf(self, pdf_bytes: any):
        pdf = BytesIO(pdf_bytes)
        pdf = fitz.open(stream=pdf, filetype="pdf")
        return pdf_to_json_pipeline(pdf)
