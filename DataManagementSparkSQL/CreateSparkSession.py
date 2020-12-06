from __future__ import print_function

from pyspark.sql import SparkSession


def create_spark_session():
    """
    Create Spark Session
    :return: Spark Session
    """
    spark = SparkSession \
        .builder \
        .appName("Twitter Analysis Pipeline") \
        .master("local[*]") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()
    return spark
