from .initialize import initialize_model
from .summary import summary
from services.spark import *
from services.redis import *
from pyspark.rdd import RDD
from .core import Core


class SummarizerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SummarizerSingleton, cls).__new__(cls)
        return cls._instance

    def summarize_chunks_in_partition(self, partition):
        core = initialize_model(Core())
        return [summary(chunk, core) for chunk in partition]

    def summarize(self, chunks: RDD) -> RDD:
        return chunks.mapPartitions(self.summarize_chunks_in_partition)
