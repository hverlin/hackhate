from webapp.apps.classifiers import HateBaseClassifier, NltkClassifier
import pandas as pd
import numpy as np


def hatebase_trump():
    classifier = HateBaseClassifier.HateBaseClassifier()
    tweets = pd.read_json("../data/trump_tweets/2013.json")
    tweet_texts = tweets["text"]
    for index, row in tweet_texts.iteritems():
        hate_word_index = classifier.classify(str(row))
        if hate_word_index:
            if True in hate_word_index:
                print(row)
                print(np.array(row.split())[np.where(hate_word_index)])

def nltk_trump():
    classifier = NltkClassifier.NltkClassifier()
    tweets = pd.read_json("../data/trump_tweets/2013.json")
    tweet_texts = tweets["text"]
    for index, row in tweet_texts.iteritems():
        scores = classifier.analyse_text(str(row))
        if scores['compound'] < -0.7:
            print(row)
            print(scores)


nltk_trump()


