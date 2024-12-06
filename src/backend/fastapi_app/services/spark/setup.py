from pyspark.sql import SparkSession


class SparkSessionSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SparkSessionSingleton, cls).__new__(cls)
            cls._instance.spark = (
                SparkSession.builder.appName("Scholarly")
                .master("local[*]")
                .getOrCreate()
            )
        return cls._instance

    def get_spark_session(self):
        return self.spark

    def get_spark_context(self):
        return self.spark.sparkContext
