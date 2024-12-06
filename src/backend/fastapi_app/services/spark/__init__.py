from .setup import SparkSessionSingleton, SparkContext, SparkSession


def get_spark_session() -> SparkSession:
    return SparkSessionSingleton().get_spark_session()


def get_spark_context() -> SparkContext:
    return SparkSessionSingleton().get_spark_context()


def stop_spark_session() -> None:
    SparkSessionSingleton().close()


__all__ = [
    "get_spark_session",
    "stop_spark_session",
    "get_spark_context",
    "SparkSessionSingleton",
]
