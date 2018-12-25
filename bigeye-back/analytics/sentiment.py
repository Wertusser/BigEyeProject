from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from utils.analytics import csv2dict

mystem = Mystem()
russian_stopwords = stopwords.words("russian")
SENTIMENT_DICT = csv2dict("/home/wertusser/PycharmProjects/bigEye/static/sentiment.csv")


def preprocess_text(text):
    tokens = mystem.lemmatize(text)
    return [token for token in tokens if token not in russian_stopwords \
            and token != " " \
            and token.strip() not in punctuation]


def get_sentiment_map(text):
    tokens = preprocess_text(text)
    result = [(token, SENTIMENT_DICT.get(token, 0)) for token in tokens]
    return result
