import tweepy
import numpy as np
import scipy.stats
from django.utils.safestring import mark_safe

from apps.classifiers import NltkClassifier
from junction_hate import settings_local as st


class TextFromTwitter():
    def __init__(self):
        consumer_key = st.TWITTER_consumer_key
        consumer_secret = st.TWITTER_consumer_secret
        access_token = st.TWITTER_access_token
        access_token_secret = st.TWITTER_access_token_secret

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def get_status_from_user_from_tweet_id(self, user, tweet_number=1, tweet_id=""):
        if tweet_id == "":
            status = self.api.user_timeline(screen_name=user, count=tweet_number)
        else:
            status = self.api.user_timeline(screen_name=user, count=tweet_number, max_id=tweet_id)

        tweet_list = []

        for s in status:
            tweet = {"id": s.id, "message": s.text}
            tweet_list.append(tweet)
        return tweet_list

    def get_status_from_user(self, user, tweet_number=1):
        return self.get_status_from_user_from_tweet_id(user=user, tweet_number=tweet_number)

    def search_first_user(self, search_user):
        users = self.api.search_users(q=search_user, count=1)
        if not users:
            return None
        else:
            return {"id": users[0].id,
                    "followers_count": users[0].followers_count,
                    "profile_image_url": users[0].profile_image_url_https,
                    "tweet_number": users[0].statuses_count,
                    "location": users[0].location,
                    "screen_name": users[0].screen_name,
                    "description": users[0].description
                    }

    def get_nltk_statistic(self, user, tweet_number=10):
        classifier = NltkClassifier.NltkClassifier()
        tweets = self.get_status_from_user(user, tweet_number=tweet_number)
        tweet_with_scores = []
        compound_scores = []
        for tweet in tweets:
            scores = classifier.analyse_text(tweet['message'])
            tweet_with_scores.append({
                'message': tweet['message'],
                'scores': scores,
            })
            compound_scores.append(scores['compound'])

        stats = {
            "labels": [""],
            "scores": [""]
        }

        try:
            stats = scipy.stats.describe(compound_scores)
        except:
            pass

        try:
            ret = {
                "tweets": tweet_with_scores,
                "stats": {
                    "labels": mark_safe(["min", "mean", "max"]),
                    "scores": [stats.minmax[0], stats.mean, stats.minmax[1]],
                }
            }
        except:
            ret = {
                "tweets": tweet_with_scores,
                "stats": stats
            }

        return ret


if __name__ == '__main__':
    twitter = TextFromTwitter()
    print(twitter.get_nltk_statistic("potus", 20))
    # print(twitter.get_nltk_statistic("realdonaldtrump", 200))
    # print(twitter.get_nltk_statistic("matthewheimbach", 200))
