import re
from urlextract import URLExtract
extractor = URLExtract()
import contractions
import nltk


def preprocess(text):
    text = str(text).lower()
    #remove urls
    urls = extractor.find_urls(text)
    for url in urls:
        text = text.replace(url, '')
    #remove emails
    text = re.sub(r'\S*@\S*\s?',' ',text)
    #remove mentions
    text = re.sub(r'@\S+', ' ', text)
    #contractions
    text = contractions.fix(text)
    #remove hashtags
    text = re.sub(r'@\S+', ' ', text)
    #remove emojis
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    #remove all punct
    text = re.sub('[^A-z0-9]', ' ', text)
    #remove extras whitespaces
    text = re.sub(' +', ' ', text)
    return text