from .setup import SparkSessionSingleton


def get_spark_session():
    return SparkSessionSingleton.get_spark_session()


def get_spark_context():
    return SparkSessionSingleton.get_spark_context()


__all__ = ["get_spark_session", "SparkSessionSingleton", "get_spark_context"]
