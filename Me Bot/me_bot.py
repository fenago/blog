import pickle
import numpy as np
from prepare_files import embed_sentence_lite, sp, MEDIA_APP

def load_file(file_path):
    f = open(file_path, 'rb')
    embeddings = pickle.load(f)
    f.close()
    return embeddings
    
other_embeddings = load_file('texts/{}/other_embeddings.p'.format(MEDIA_APP))
your_embeddings = load_file('texts/{}/your_embeddings.p'.format(MEDIA_APP))
pr_to_sp = load_file('texts/{}/dilogues.p'.format(MEDIA_APP))
your_sentences = load_file('texts/{}/your_sents.p'.format(MEDIA_APP))
key_embeddings = load_file('texts/{}/key_embeddings.p'.format(MEDIA_APP))
keys = list(pr_to_sp.keys())


def find_closest(sentence_rep,query_rep,K):
    top_K = np.argsort(np.sqrt((np.sum(np.square(sentence_rep - query_rep),axis=1))))[:K]
    return top_K

def speak_like_me(query, K):
    print(query)
    other_query = [query]
    sentences = []
    query_embedding = embed_sentence_lite(other_query)
    closest_your = find_closest(your_embeddings,query_embedding,K)
    for cl in closest_your:
        sentences.append(your_sentences[cl])

    return sentences
        
def respond_like_me(query, K):
    other_query = [query]
    sentences = []
    query_embedding = embed_sentence_lite(other_query)
    closest_other = find_closest(key_embeddings,query_embedding,K+2)
    for k in closest_other[3:]:
        sentences.append(pr_to_sp[keys[k]])

    return sentences