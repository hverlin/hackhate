import pandas as pd
import re


class HateBaseClassifier:
    """
    Allows to classifiy given strings by appereance in the hatebase data.
    """

    def __init__(self, data="apps/data/hatebase/vocabulary.json"):
        import os
        cwd = os.getcwd()
        print(cwd)
        self.hatebase = pd.read_json(data)

    def classify(self, message):
        """
        Classify every word in given message as hate or not

        :param message:
        :return: list of booleans for every word
        """
        try:
            return list(map(self.is_hate_word, message.split()))
        except Exception:
            print("Error with message" + message)

    def classify_with_info(self, message):
        """
        Classify every word in given message with additional information

        :param message:
        :return: list of dict
        """
        hate_info = []
        for word in message.split():
            info = self.get_hate_word_info(word)
            if info:
                hate_info.append(self.get_hate_word_info(word))
        return hate_info

    def is_hate_word(self, word):
        """
        Check if word is contained in hatebase data.
        :param word:
        :return: boolean
        """
        word = str.lower(word)
        word = word.strip('"').strip("'")
        reg_w = re.compile("^{0};|^{0}$".format(re.escape(word)))
        return len(self.hatebase[(self.hatebase["variants"].str.match(reg_w, case="False", na=False)) |
                                 (self.hatebase["vocabulary"].str.match(reg_w, case="False"))]) > 0

    def get_hate_word_info(self, word):
        word = str.lower(word)
        word = word.strip('"').strip("'")
        reg_w = re.compile("^{0};|^{0}$".format(re.escape(word)))
        df = self.hatebase[(self.hatebase["variants"].str.match(reg_w, case="False", na=False)) |
                           (self.hatebase["vocabulary"].str.match(reg_w, case="False"))]
        if not df.empty:
            df = df.iloc[0]
            return {'word': word, 'meaning': df["meaning"], 'offensiveness': df["offensiveness"]}

