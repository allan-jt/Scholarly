from services.spark import *
from services.redis import *
from pyspark.rdd import RDD
from .pdf_parser import *
import requests
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

    async def chunker(self, request_id: str):
        redis_db = get_redis_pdfs()
        pdfs = await redis_db.lrange(request_id, 0, -1)
        if not pdfs:
            return []

        sparkContext = get_spark_context()
        rdd = sparkContext.parallelize(pdfs)
        return rdd.map(self.chunk_pdf).collect()
