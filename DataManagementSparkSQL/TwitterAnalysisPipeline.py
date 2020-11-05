from __future__ import print_function

import os
import glob
import pyspark
import preprocessor as p
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from DataManagementSparkSQL.us_state_abbrev import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import nltk
nltk.download('vader_lexicon')


def create_spark_session():
    """
    Create Spark Session
    :return:
    """
    spark = SparkSession \
        .builder \
        .appName("Twitter Analysis Pipeline") \
        .master("local[4]") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()
    return spark


class TwitterAnalysisPipeline(object):
    """
    This class is load the twitter log to a Spark SQL Dataframe table, and do the following things
        1. Remove the tweets contains no location
        2. Create column indicate the state of the twitter (They have the massive location format!)
        3. Write to the filesystem with parquet table format

    """

    def __init__(self, event_log_dir: str):
        """
        :param event_log_dir: Dir contains the twitter logs
        """
        self.event_log_dir = event_log_dir
        self.spark = create_spark_session()
        self.tweets_dataframe: pyspark.sql.DataFrame = self.load_ori_tweets_dataframe()

    def load_ori_tweets_dataframe(self):
        """
        Get all original tweets log files and load as a Spark sql Dataframe
        """
        tweets_log_files = glob.glob(os.path.join(self.event_log_dir, '*.txt'))
        print("Load Dataframe from the following files: {}".format(tweets_log_files))
        self.tweets_dataframe = self.spark.read.json(tweets_log_files) \
                                    .drop('user_id', 'urls', 'country', 'hashtags', 'location type') \
                                    .withColumnRenamed('user_screen _name', 'user_screen_name')
        # ori_tweets_dataframe.show(50, False)
        print("Total Tweets in the log are: {}".format(self.tweets_dataframe.count()))
        return self.tweets_dataframe

    def __determine_state_dataframe(self):
        """
        Determine the state of each tweet, and filter the None
        """

        # Broadcast the state abbrev dict to speed up and avoid data shuffle
        us_state_abbrev_bc = self.spark.sparkContext.broadcast(us_state_abbrev)

        # Function to Determine the state of the locations
        def determine_state(location):
            us_state_abbrev_bc_value = us_state_abbrev_bc.value
            for state, abbrev in us_state_abbrev_bc_value.items():
                if state.lower() in location.lower() or abbrev in location:
                    return state
            return None

        # Register the user-defined function
        udf_function_state = udf(lambda col_location: determine_state(col_location), StringType())
        # Apply the udf to the column 'location' and get the 'state' column
        self.tweets_dataframe = self.tweets_dataframe\
                                    .filter(col('location').isNotNull()) \
                                    .withColumn('state', udf_function_state(col('location'))) \
                                    .filter(col('state').isNotNull())
        print("Total Tweets can determine the state are: {}".format(self.tweets_dataframe.count()))
        return self

    def __determine_candidate_dataframe(self):
        """
        Determine the candidate of each tweet, add two columns, biden and trump,
        contains boolean value indicate whether the tweet related to each candidate
        """

        # Register the user-defined function
        udf_function_biden = udf(lambda col: ('joe' in col.lower()) or ('biden' in col.lower()), BooleanType())
        udf_function_trump = udf(lambda col: ('donald' in col.lower()) or ('trump' in col.lower()), BooleanType())
        # Apply the udf to the column 'text' and get the 'biden', 'trump' column
        self.tweets_dataframe = self.tweets_dataframe \
                                    .withColumn('biden', udf_function_biden(col('text'))) \
                                    .withColumn('trump', udf_function_trump(col('text')))
        return self

    def __tweet_clean_dataframe(self):
        """
        Clean the Tweet text column
        Remove url, mention, hashtag, reserved words, Emoji, Smiley, number, escape char
        """

        # Function to clean the tweets
        def tweet_clean(text):
            # Regex based tweet clean package
            return p.clean(text).strip(" :")

        # Register the user-defined function
        udf_function_clean = udf(lambda col: tweet_clean(col), StringType())
        # Apply the udf to the 'text' column
        self.tweets_dataframe = self.tweets_dataframe.withColumn('text', udf_function_clean(col('text')))
        return self

    def __sentiment_analysis(self):
        """
        Do sentiment analysis over the text columns, use Vader
        """

        # Function to clean the tweets
        def tweet_sentiment(text):
            analyzer = SentimentIntensityAnalyzer()
            vs = analyzer.polarity_scores(text)
            return vs

        # Register the user-defined function
        udf_function_sentiment = udf(lambda col: tweet_sentiment(col), MapType(StringType(), DoubleType()))
        # Apply the udf to the 'text' column
        self.tweets_dataframe = self.tweets_dataframe \
                                    .withColumn('sentiment', udf_function_sentiment(col('text'))) \
                                    .withColumn('sentiment_neg', col('sentiment').getItem('neg')) \
                                    .withColumn('sentiment_pos', col('sentiment').getItem('pos')) \
                                    .withColumn('sentiment_compound', col('sentiment').getItem('compound')) \
                                    .withColumn('sentiment_neu', col('sentiment').getItem('neu')) \
                                    .drop('sentiment')
        return self

    def whole_pipeline(self):
        """
        Preprocessing and sentiment analysis over the dataframe
        """
        self.__determine_state_dataframe()\
            .__determine_candidate_dataframe()\
            .__tweet_clean_dataframe()\
            .__sentiment_analysis()
        return self.tweets_dataframe

    def save_dataframe_parquet(self, target_dir):
        self.tweets_dataframe.write.partitionBy('state').mode('overwrite').parquet(target_dir)
        return self


def main():
    twitter_analysis_pipeline = TwitterAnalysisPipeline('/Users/yuanbincheng/Desktop/TwitterLogs/')
    tweets_dataframe = twitter_analysis_pipeline.whole_pipeline()
    tweets_dataframe.show(20, False)
    twitter_analysis_pipeline.save_dataframe_parquet('/Users/yuanbincheng/Desktop/TweetProcessedTable/')
    # tweets_dataframe.printSchema()


if __name__ == '__main__':
    main()
