from services.spark import *
from services.redis import *
from pyspark.rdd import RDD
from .pdf_parser import *
import requests


class ChunkerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChunkerSingleton, cls).__new__(cls)
        return cls._instance

    def chunker(self, pdfs: RDD) -> RDD:
        pass
