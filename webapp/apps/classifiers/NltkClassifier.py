from typing import Dict
import scipy.stats

from nltk.sentiment.vader import SentimentIntensityAnalyzer


class NltkClassifier:
    """
    Classify entire strings with nltk's Vader API.
    """

    def __init__(self):
        self._analyser = SentimentIntensityAnalyzer()

    def analyse_text(self, txt: str) -> Dict[str, float]:
        """
        Analyse a text.
        :param txt: a string
        :return: A dictionary with 4 entries:
            'compound', 'negative', 'neu', 'pos'
        """
        score = self._analyser.polarity_scores(txt)
        score['negative'] = score['neg'] * (-1)
        score.pop("neg", None)
        return score

    def is_negative(self, txt: str) -> bool:
        """
        Return True if the text is negative
        """
        res = self.analyse_text(txt)
        return res['compound'] < 0

    def is_positive(self, txt: str) -> bool:
        """
        Return True if the text is positive
        """
        res = self.analyse_text(txt)
        return res['compound'] > 0

    def get_statistic(self, messages):
        """
        Returns statistic on compound value on a list of messages

        :param messages: list of messages
        :return: DescribeResult
        """
        compound_scores = []
        for message in messages:
            scores = self.analyse_text(message)
            compound_scores.append(scores['compound'])
        return scipy.stats.describe(compound_scores)
