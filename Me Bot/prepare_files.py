import sys
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import warnings
import pickle
import sentencepiece as spm

MEDIA_APP ='whatsapp'
module_url = "https://tfhub.dev/google/universal-sentence-encoder-lite/2"


module = hub.Module(module_url)
input_placeholder = tf.compat.v1.sparse_placeholder(tf.int64, shape=[None, None])
encodings = module(
    inputs=dict(
        values=input_placeholder.values,
        indices=input_placeholder.indices,
        dense_shape=input_placeholder.dense_shape))

with tf.Session() as sess:
    spm_path = sess.run(module(signature="spm_path"))

sp = spm.SentencePieceProcessor()
sp.Load(spm_path)



def process_to_IDs_in_sparse_format(sentences):
    ids = [sp.EncodeAsIds(x) for x in sentences]
    max_len = max(len(x) for x in ids)
    dense_shape=(len(ids), max_len)
    values=[item for sublist in ids for item in sublist]
    indices=[[row,col] for row in range(len(ids)) for col in range(len(ids[row]))]
    return (values, indices, dense_shape)

def embed_sentence_lite(sentences):
    values, indices, dense_shape = process_to_IDs_in_sparse_format(sentences)


    with tf.Session() as session:
        session.run([tf.compat.v1.global_variables_initializer(), tf.compat.v1.tables_initializer()])
        message_embeddings = session.run(
          encodings,
          feed_dict={input_placeholder.values: values,
                    input_placeholder.indices: indices,
                    input_placeholder.dense_shape: dense_shape})
    
    return message_embeddings

def write_embeddings_to_file(whose='your'):
    f = open('texts/{}/{}_sents.p'.format(MEDIA_APP, whose), 'rb')
    your_sentences = pickle.load(f)
    f.close()

    list_embeds = []
    for i in range(0,len(your_sentences),500):
        list_embeds.append(embed_sentence_lite(your_sentences[i:i+500]))

    embeddings = np.vstack(list_embeds)
    
    f = open('texts/{}/{}_embeddings.p'.format(MEDIA_APP, whose), 'wb')
    pickle.dump(embeddings,f)
    f.close()
    
def write_dialogues_to_file(file_name):
    f =  open('texts/{}/dilogues.p'.format(MEDIA_APP),'rb')
    you_to_other = pickle.load(f)
    
    keys = list(you_to_other.keys())

    list_embeds = []
    for i in range(0,len(keys),500):
        list_embeds.append(embed_sentence_lite(keys[i:i+500]))

    key_embeddings = np.vstack(list_embeds)

    f = open('texts/{}/{}'.format(MEDIA_APP, file_name),'wb')
    pickle.dump(key_embeddings,f)
    f.close()
    
    
write_embeddings_to_file(whose='your')
write_embeddings_to_file(whose='other')
write_dialogues_to_file(file_name='key_embeddings.p')