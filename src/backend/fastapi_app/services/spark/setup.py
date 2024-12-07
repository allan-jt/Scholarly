from pyspark.sql import SparkSession
from pyspark import SparkContext
import os


class SparkSessionSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SparkSessionSingleton, cls).__new__(cls)
            cls._instance.spark = (
                SparkSession.builder.appName(os.getenv("SPARK_APP_NAME"))
                .master(os.getenv("SPARK_MASTER"))
                .getOrCreate()
            )
        return cls._instance

    def get_spark_session(self) -> SparkSession:
        return self.spark

    def get_spark_context(self) -> SparkContext:
        return self.spark.sparkContext

    def close(self) -> None:
        self.spark.stop()
        self._instance = None
