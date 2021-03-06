import nltk, string
from nltk.stem import PorterStemmer

nltk.download('stopwords')
from nltk.corpus import stopwords


def remove_stopwords(text):
    stopwords_english = stopwords.words('english')
    new_text = ' '.join([char for char in text.split() if char not in stopwords_english])
    return new_text

def remove_punctuation(text):
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    return text.lower().translate(remove_punctuation_map)

def tokenize(text):
    return nltk.word_tokenize(text)

def stem_tokens(tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(item) for item in tokens]


def clean(text):
    new_text = remove_stopwords(text)
    new_text = remove_punctuation(new_text)
    tokens = tokenize(new_text)
    stemmed_tokens = stem_tokens(tokens)
    return stemmed_tokens