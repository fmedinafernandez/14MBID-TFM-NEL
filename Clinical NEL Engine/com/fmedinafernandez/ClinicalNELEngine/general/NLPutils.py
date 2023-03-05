'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''
import os
import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
#!pip install gensim
from gensim.models import FastText
#! pip install spacy
#! python -m spacy download es
#! pip install transformers
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import spacy
#import es_core_news_sm
#python -m spacy download es_core_news_sm

#!pip install tensorflow
#!pip install tensorflow_hub
#!pip install bert-tensorflow
import tensorflow_hub as hub
import tensorflow as tf
from tensorflow.keras.models import Model 
import bert
# BETO tokenizer
#!pip install keras_bert
from keras_bert import load_vocabulary, Tokenizer
from keras_bert import load_trained_model_from_checkpoint
model_path = "com\\fmedinafernandez\\ClinicalNELEngine\\models\\BETO-Galen\\"
#https://github.com/dccuchile/beto/blob/master/config/uncased_2M/config.json
config_path = model_path + "config.json"
#https://github.com/guilopgar/ClinicalCodingTransformerES/tree/main/BETO/BETO-Galen
checkpoint_path = model_path + "model.ckpt-1000000"
#https://github.com/dccuchile/beto/blob/master/config/uncased_2M/vocab.txt
vocab_file = "vocab.txt"
# Hyper-parameters
training = False
trainable = True
SEQ_LEN = 128


import numpy as np
from numpy.linalg import norm
from operator import itemgetter


def preprocessDoc(doc):
  logs.log('NLPutils.preprocessDoc("' + doc + '")')

  #Cargamos el modelo en español
  #nlp = spacy.load("es_core_news_sm")

  #Tokenizado
  doc = [" ".join([token.text for token in nlp(doc)])][0]

  #Eliminación de signos de puntuación
  doc = [" ".join([token.lemma_ for token in nlp(doc) if not token.is_punct]) ][0]

  #Eliminación de stopwords
  spacy_stopwords = spacy.lang.es.stop_words.STOP_WORDS
  doc = [" ".join([token for token in doc.split() if not token.lower() in spacy_stopwords])][0]
  
  #Lematización de palabras
  doc = [" ".join([token.lemma_ for token in nlp(doc)])][0]

  #Eliminación de tildes
  tildes = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'Á': 'A', 'E': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'ü': 'u', 'Ü': 'U'}
  for tilde in tildes:
	  if tilde in doc:
		  doc = doc.replace(tilde, tildes[tilde])

  return doc.strip()

def getembedding(termino):
    #logs.log("NLPutils.getembedding('"+ termino +"')")
    #Devolvemos la media de los vectores densos de las palabras que componen el término
    embeddings = []
    for word in termino.split():
        embeddings.append(modelFastText.wv.get_vector(word))
    return np.mean(embeddings, axis=0)
    #return modelFastText.wv.get_vector(termino)

def calculateCosineSimilarity(embedding_A, embedding_B):	
	#logs.log('NLPutils.calculateCosineSimilarity(embedding_A, embedding_B)')
	cosine = np.dot(embedding_A,embedding_B)/(norm(embedding_A)*norm(embedding_B))
	return cosine

def NLP_get_ngrams(text, n):
	#logs.log('NLPutils.NLP_get_ngrams("'+ text + '", ' + str(n) +')')
	text = text.split()
	output = []
	for i in range(len(text) - n + 1):
		output.append(text[i:i+n])
	return output

#def NLP_get_labels(doc):
#	informe_preprocesado = NLP_preprocesaDocumento(informe)

def split_sentences(text):
	#logs.log('NLPutils.split_sentences("'+ text +'")')
	tokens = nlp(text)
	sentences = []
	for sent in tokens.sents:
		sentences.append(sent.text.strip())
	return sentences


# See BERT paper: https://arxiv.org/pdf/1810.04805.pdf
# And BERT implementation convert_single_example() at https://github.com/google-research/bert/blob/master/run_classifier.py

def get_masks(tokens, max_seq_length):
    """Mask for padding"""
    if len(tokens)>max_seq_length:
        raise IndexError("Token length more than max seq length!")
    return [1]*len(tokens) + [0] * (max_seq_length - len(tokens))


def get_segments(tokens, max_seq_length):
    """Segments: 0 for the first sequence, 1 for the second"""
    if len(tokens)>max_seq_length:
        raise IndexError("Token length more than max seq length!")
    segments = []
    current_segment_id = 0
    for token in tokens:
        segments.append(current_segment_id)
        if token == "[SEP]":
            current_segment_id = 1
    return segments + [0] * (max_seq_length - len(tokens))


def get_ids(text, tokens, tokenizer, max_seq_length):
    """Token ids from Tokenizer vocab"""
    #token_ids = tokenizer.convert_tokens_to_ids(tokens)
    token_ids = tokenizer.encode(text)[0]
    input_ids = token_ids + [0] * (max_seq_length-len(token_ids))
    return input_ids

def getembedding_Transformer(text):
	logs.log('NLPutils.getembedding_Transformer("'+ text +'")')
	tokens = tokenizerTransformer.tokenize(text)
	input_ids = get_ids(text, tokens, tokenizerTransformer, SEQ_LEN)
	input_masks = get_masks(tokens,SEQ_LEN)
	input_segments = get_segments(tokens,SEQ_LEN)
	input_ids_tensor = tf.reshape(tf.convert_to_tensor(input_ids), [1, SEQ_LEN])
	input_masks_tensor = tf.reshape(tf.convert_to_tensor(input_masks), [1, SEQ_LEN])
	input_segments_tensor = tf.reshape(tf.convert_to_tensor(input_segments), [1, SEQ_LEN])
	embeddings = modelTransformer.predict([[input_ids_tensor],[input_segments_tensor]])
	return np.mean(embeddings[0],axis=0)
	
def loadmodel_NLP():
	logs.log("NLPutils.loadmodel_NLP()")

	#python -m spacy download es_core_news_sm
	#nlp = spacy.load("es_core_news_sm")
	nlp = spacy.load("es_core_news_lg")
	#nlp = es_core_news_sm.load()
	return nlp

def loadmodel_FastText():
	logs.log("NLPutils.loadmodel_FastText()")

	#El fichero .vec, nos vale sólo para palabras exactas
	#Necesitamos usar el modelo .bin, para poder extraer el embedding de palabras nuevas
	modelFastText = FastText.load_fasttext_format('com\\fmedinafernandez\\ClinicalNELEngine\\models\\FastText\\clinic_es.bin')
	return modelFastText

def loadmodel_Transformer():
	logs.log("NLPutils.loadmodel_Transformer()")


	#Cargamos el modelo de BETO-Galen
	modelTransformer = load_trained_model_from_checkpoint(
          config_file=config_path,
          checkpoint_file=checkpoint_path,
          training=training,
          trainable=trainable,
          seq_len=SEQ_LEN
        )
	return modelTransformer

#Cargamos los modelos de NLP
nlp = loadmodel_NLP()
modelFastText = loadmodel_FastText()
#tokenizerTransformer = Tokenizer(token_dict=load_vocabulary(model_path + vocab_file), pad_index=1, cased=True)
#modelTransformer = loadmodel_Transformer()



