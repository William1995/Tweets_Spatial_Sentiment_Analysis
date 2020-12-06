from __future__ import print_function

import os
import glob
import pyspark
import preprocessor as p
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, col, count
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from us_state_abbrev import *
from CreateSparkSession import create_spark_session


def load_table(spark: SparkSession, twitter_table_dir):
    df = spark.read.parquet(twitter_table_dir)
    return df


def total_tweet_count(df: DataFrame):
    biden_count = df.filter(df.biden).groupBy('state').agg(count('*').alias('biden_count'))
    trump_count = df.filter(df.trump).groupBy('state').agg(count('*').alias('trump_count'))
    total_count_ret = biden_count.join(trump_count, biden_count['state'] == trump_count['state'], 'inner') \
        .select(biden_count.state, "biden_count", "trump_count")
    total_count_ret.show(100, False)
    return total_count_ret


def tweet_sentiment_count(df: DataFrame):
    biden_positive_count = df.filter(df.biden).filter(df.sentiment_compound > 0.05) \
        .groupBy('state').agg(count('*').alias('biden_positive_count'))
    biden_negative_count = df.filter(df.biden).filter(df.sentiment_compound < -0.05) \
        .groupBy('state').agg(count('*').alias('biden_negative_count'))
    biden_sentiment_ret = biden_positive_count \
        .join(biden_negative_count, biden_positive_count['state'] == biden_negative_count['state']) \
        .select(biden_positive_count.state, "biden_positive_count", "biden_negative_count")

    trump_positive_count = df.filter(df.trump).filter(df.sentiment_compound > 0.05) \
        .groupBy('state').agg(count('*').alias('trump_positive_count'))
    trump_negative_count = df.filter(df.trump).filter(df.sentiment_compound < -0.05) \
        .groupBy('state').agg(count('*').alias('trump_negative_count'))
    trump_sentiment_ret = trump_positive_count \
        .join(trump_negative_count, trump_positive_count['state'] == trump_negative_count['state']) \
        .select(trump_positive_count.state, "trump_positive_count", "trump_negative_count")

    final_sentiment_ret = biden_sentiment_ret \
        .join(trump_sentiment_ret, biden_sentiment_ret['state'] == trump_sentiment_ret['state']) \
        .select(biden_sentiment_ret.state, "biden_positive_count", "biden_negative_count",
                "trump_positive_count", "trump_negative_count")

    final_sentiment_ret.show(100, False)
    return final_sentiment_ret


def main():
    spark = create_spark_session()

    df = load_table(spark, '/Users/yuanbincheng/Desktop/TweetProcessedTableBefore/')
    total_count_ret = total_tweet_count(df)
    final_sentiment_ret = tweet_sentiment_count(df)
    total_count_ret.coalesce(1).write.mode("overwrite").csv("./TweetsAnalysisResults/Total_Count_Before", header=True)
    final_sentiment_ret.coalesce(1).write.mode("overwrite").csv("Sentiment_Count_Before", header=True)

    df = load_table(spark, '/Users/yuanbincheng/Desktop/TweetProcessedTableDuring/')
    total_count_ret = total_tweet_count(df)
    final_sentiment_ret = tweet_sentiment_count(df)
    total_count_ret.coalesce(1).write.mode("overwrite").csv("./TweetsAnalysisResults/Total_Count_During", header=True)
    final_sentiment_ret.coalesce(1).write.mode("overwrite").csv("Sentiment_Count_During", header=True)


if __name__ == '__main__':
    main()
