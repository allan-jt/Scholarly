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

    def summarize_chunked_sections(self, chunked_sections: RDD) -> RDD:
        def summarize_chunks_in_partition(partition):
            core = initialize_model(Core())

            for chunk in partition:
                header = chunk["header"]
                text = chunk["text"]
                summarized_chunk = summary(text, core)
                yield {"header": header, "summary": summarized_chunk["final_summary"]}

        return chunked_sections.mapPartitions(summarize_chunks_in_partition)
