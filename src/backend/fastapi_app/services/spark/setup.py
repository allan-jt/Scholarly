from pyspark.sql import SparkSession
from pyspark import SparkContext
import os


class SparkSessionSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # REQUIREMENTS_FILE = os.path.join(
            #     os.path.dirname(__file__), "../../requirements.txt"
            # )
            # print("Requirements file contents:")
            # with open(REQUIREMENTS_FILE, "r") as f:
            #     print(f.read())
            cls._instance = super(SparkSessionSingleton, cls).__new__(cls)
            cls._instance.spark = (
                SparkSession.builder.appName(os.getenv("SPARK_APP_NAME")).master(
                    os.getenv("SPARK_MASTER")
                )
                # .config("spark.submit.pyFiles", REQUIREMENTS_FILE)
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
