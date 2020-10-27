import os
import sys
import json
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener


ACCESS_TOKEN = '175301009-zXwe95IdcIO5YhDK5DxJcgo8aVlCpp8K0tHHsF8f'
ACCESS_TOKEN_SECRET = 't25mm63g6hhCNVGWe2UqtlTxU8elCLYB363MVbiYr51jG'
CONSUMER_KEY = 'PkSrfrHn6rktNRBB6R3aYSFOR'
CONSUMER_SECRET = 'SDxB9y42hSUnaXt3vkGxGPY3kL7TgYqnHxth2sZP0n2KtmYNoS'


def get_auth_api(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET):
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = API(auth, wait_on_rate_limit=True,
              wait_on_rate_limit_notify=True)
    return api


class StreamWatcherListener(StreamListener):
    def __init__(self, output_file):
        super(StreamWatcherListener, self).__init__()
        self.output_file = open(output_file, 'w')

    def on_status(self, status):
        # Tweet information we want to get
        tweet = {"created_at": str(status.created_at),
                 "user_id": status.user.id,
                 "user_screen _name": status.user.screen_name,
                 "hashtags": status.entities['hashtags'],
                 "urls": status.entities['urls']}
        # If the text is cut because of the length
        if hasattr(status, 'extended_tweet'):
            tweet["text"] = status.extended_tweet["full_text"]
        else:
            tweet["text"] = status.text
        # If the tweet contains the location information
        if status.place is not None:
            tweet["location"] = status.place.full_name
            tweet["location type"] = status.place.place_type
            tweet["country"] = status.place.country_code
        else:
            # Use the user's location
            if status.user.geo_enabled is True:
                tweet["location"] = status.user.location
            # No Geo Info, ignore this tweet
            else:
                return
        tweet_json = json.dumps(tweet)
        self.output_file.write(tweet_json + '\n')
        # print(tweet_json)

    def on_error(self, status_code):
        print(status_code)
        return False


def main():
    api = get_auth_api(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    listener = StreamWatcherListener("TweetsLog.txt")
    stream = Stream(auth=api.auth, tweet_mode='extended', listener=listener)

    try:
        print('Start streaming.')
        stream.filter(track=["joe biden", 'donald trump'], languages=["en"])
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        print('Done.')
        stream.disconnect()


if __name__ == '__main__':
    main()