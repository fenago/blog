from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from utils import clean

def read_file(path):
    file = open(path, mode='r')
    text = file.read()
    return text.replace('\n', '')

def calc_cosine_sim(path_1, path_2):
    text_1 = read_file(path_1)
    text_2 = read_file(path_2)
    
    cleaned_sentences = list(map(lambda x: ' '.join(clean(x)), [text_1, text_2]))

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(cleaned_sentences)

    vectors = counts.toarray()

    vec_1 = vectors[0].reshape(1, -1)
    vec_2 = vectors[1].reshape(1, -1)
    
    return cosine_similarity(vec_1, vec_2)[0][0]