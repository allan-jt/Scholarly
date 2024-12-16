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

    def summarize_pdfs(self, pdfs: RDD) -> RDD:
        def summarize_pdfs_in_partition(partition):
            core = initialize_model(Core())

            for i, pdf in enumerate(partition):
                for chunk in pdf:  # Iterate over chunks in the PDF
                    header = chunk["header"]
                    text = chunk["text"]
                    summarized_chunk = summary(text, core)
                    yield (i, header, summarized_chunk)  # Yield results

        return pdfs.mapPartitions(summarize_pdfs_in_partition)
