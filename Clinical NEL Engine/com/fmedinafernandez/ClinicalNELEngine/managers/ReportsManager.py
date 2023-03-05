#!/usr/local/bin/python
# coding: latin-1
'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''

from time import localtime, strftime
import random
import os
from shutil import copyfile
import numpy as np
from operator import itemgetter

import com.fmedinafernandez.ClinicalNELEngine.general.utils as utils
import com.fmedinafernandez.ClinicalNELEngine.general.exceptions as exceptions
import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
import com.fmedinafernandez.ClinicalNELEngine.general.NLPutils as nlputils
import com.fmedinafernandez.ClinicalNELEngine.general.configuration as configuration
import com.fmedinafernandez.ClinicalNELEngine.general.constants as constants
import com.fmedinafernandez.ClinicalNELEngine.database.ReportsDAO as reportsDAO
import com.fmedinafernandez.ClinicalNELEngine.database.TerminosClinicosDAO as terminosclinicosDAO


def create_report(user, remote_addr, reportid, reportbody, model=0):
    logs.logV(user, 'ReportsManager.create_report("'+user+'","'+ remote_addr + '","'+str(reportid) + '","'+str(reportbody)+ '",'+str(model)+')')

    report_id = reportsDAO.create_report('name', user, reportid, reportbody)

	
    #La magia
    terminos_vinculados = []
	
    #DESERIALIZAR EL EMBEDDING DE CADA TERMINO DE JSON/STRING A NPARRAY
    if model == 0: #constants.FASTTEXT_MODEL:
        terminos_vinculados = get_terminosclinicos_FastText(user, reportbody)
    elif model == 1: #constants.TRANSFORMER_MODEL:
        terminos_vinculados = get_terminosclinicos_Transformer(user, reportbody)

    for termino in terminos_vinculados:
        reportsDAO.create_termino_report(report_id, termino["source_text"], termino["idtermino"], termino["cosine"], model)
	
    return report_id

			
def get_terminosclinicos_FastText(user, reportbody):
    logs.logV(user, 'ReportsManager.get_terminosclinicos_FastText("'+reportbody+'")')

    terminos_snomedct_problemassaludAH = terminosclinicosDAO.select_terminosclinicos()

    for termino in terminos_snomedct_problemassaludAH:
        termino['embedding'] = utils.deserialiceNumpyArray(termino['embedding']) 

    #Troceamos en frases el contenido del informe
    frases = nlputils.split_sentences(reportbody)
    terminos_vinculados = []
    for frase in frases:
        preprocessed_reportbody = nlputils.preprocessDoc(frase)
    
        #Empezamos por ngramas más grandes a más pequeños
        for num_ngrams in range(6, 0, -1):
            ngramas = nlputils.NLP_get_ngrams(preprocessed_reportbody, num_ngrams)
            for ngrama in ngramas:
                doc = " ".join([token for token in ngrama])
                #print(doc)
                doc_embedding = nlputils.getembedding(doc)
                vector_A = doc_embedding
                num_palabras_A = len(ngrama)
                #Por cada término de la terminología, comprobamos la similaridad con el ngrama previo
                terminos_candidatos = []
                for termino in terminos_snomedct_problemassaludAH:
                    vector_B = termino["embedding"]
                    num_palabras_B = termino["num_palabras"]
                    #Comparamos t�rminos con el mismo n�mero de palabras
                    if num_palabras_A == num_palabras_B:
                        cosine = nlputils.calculateCosineSimilarity(vector_A, vector_B)
                        if cosine > 0.9: #configuration.COSINE_SIMILARITY_PERCENTAGE_THRESHOLD:
                            print(doc, " ", termino["termino"], " Cosine Similarity:", cosine)
                            terminos_candidatos.append({"source_text": doc, "idtermino": termino["idtermino"], "termino": termino["termino"], "embedding": termino["embedding"], "cosine": cosine})
                #Nos quedamos con el término con mayor similaridad de los obtenidos
                if terminos_candidatos:
                    terminos_candidatos_sorted = sorted(terminos_candidatos, key=itemgetter('cosine'), reverse=True) 
                    terminos_vinculados.append(terminos_candidatos_sorted[0])

    #Eliminamos duplicados
    terminos_vinculados_sorted = sorted(terminos_vinculados, key=itemgetter('termino'))
    termino_ant = {"source_text":"", "idtermino":"", "termino":"", "cosine": "0.0"}
    terminos_vinculados_deduplicated = []
    for termino in terminos_vinculados_sorted:
        if termino["termino"] != termino_ant["termino"]:
            if termino_ant["termino"] != "":
                terminos_vinculados_deduplicated.append(termino_ant)
                print(termino_ant["termino"], " Cosine Similarity:", termino_ant["cosine"])
            termino_ant = termino
        else:
            if termino_ant["cosine"]<termino["cosine"]:
                termino_ant = termino
    terminos_vinculados_deduplicated.append(termino_ant)
    print(termino_ant["termino"], " Cosine Similarity:", termino_ant["cosine"])
    
    return terminos_vinculados_deduplicated

def get_terminosclinicos_Transformer(user, reportbody):
    logs.logV(user, 'ReportsManager.get_terminosclinicos_Transformer("'+reportbody+'")')

    terminos_snomedct_problemassaludAH = terminosclinicosDAO.select_terminosclinicos()

    for termino in terminos_snomedct_problemassaludAH:
        termino['embedding'] = utils.deserialiceNumpyArray(termino['embedding2']) 
    
    #Troceamos en frases el contenido del informe
    frases = nlputils.split_sentences(reportbody)
    terminos_vinculados = []
    for frase in frases:
        preprocessed_reportbody = nlputils.preprocessDoc(frase)
    
		#Empezamos por ngramas más grandes a más pequeños
        for num_ngrams in range(6, 1, -1):
            ngramas = nlputils.NLP_get_ngrams(preprocessed_reportbody, num_ngrams)
            for ngrama in ngramas:
                doc = " ".join([token for token in ngrama])
                #print(doc)
                doc_embedding = nlputils.getembedding_Transformer(doc)
                vector_A = doc_embedding
                #Por cada término de la terminología, comprobamos la similaridad con el ngrama previo
                terminos_candidatos = []
                for termino in terminos_snomedct_problemassaludAH:
                    vector_B = termino["embedding"]
                    cosine = nlputils.calculateCosineSimilarity(vector_A, vector_B)
                    if cosine > 0.94: #configuration.COSINE_SIMILARITY_PERCENTAGE_THRESHOLD:
                        print(doc, " ", termino["termino"], " Cosine Similarity:", cosine)
                        terminos_candidatos.append({"source_text": doc, "idtermino": termino["idtermino"], "termino": termino["termino"], "embedding": termino["embedding"], "cosine": cosine})
		            #Nos quedamos con el término con mayor similaridad de los obtenidos
                    if terminos_candidatos:
                        terminos_candidatos_sorted = sorted(terminos_candidatos, key=itemgetter('cosine'), reverse=True) 
                        terminos_vinculados.append(terminos_candidatos_sorted[0])

    #Eliminamos duplicados
    terminos_vinculados_sorted = sorted(terminos_vinculados, key=itemgetter('termino'))
    termino_ant = {"source_text":"", "idtermino":"", "termino":"", "cosine": "0.0"}
    terminos_vinculados_deduplicated = []
    for termino in terminos_vinculados_sorted:
        if termino["termino"] != termino_ant["termino"]:
            if termino_ant["termino"] != "":
                terminos_vinculados_deduplicated.append(termino_ant)
                print(termino_ant["termino"], " Cosine Similarity:", termino_ant["cosine"])
            termino_ant = termino
        else:
            if termino_ant["cosine"]<termino["cosine"]:
                termino_ant = termino
    terminos_vinculados_deduplicated.append(termino_ant)
    print(termino_ant["termino"], " Cosine Similarity:", termino_ant["cosine"])
    
    return terminos_vinculados_deduplicated


def get_reports(user, remote_addr, idreport='', owner='', termino=''):
    logs.logV(user, 'ReportsManager.get_reports("'+user+'","'+ remote_addr +'","'+ idreport +'","'+ owner+'","'+ termino+'")')
    return reportsDAO.get_reports(user, True, idreport, owner, termino)

def get_reports_and_labels(user, remote_addr, idreport='', owner='', termino=''):
    logs.logV(user, 'ReportsManager.get_reports("'+user+'","'+ remote_addr +'","'+ idreport +'","'+ owner+'","'+ termino+'")')
    return reportsDAO.get_reports_and_labels(user, True, idreport, owner, termino)


def get_termino_reports(user, remote_addr, report_id):
    logs.logV(user, 'ReportsManager.get_termino_reports('+user+'","'+ remote_addr +'","'+str(report_id)+'")')
    return reportsDAO.select_termino_reports(report_id)

def select_reports(user, remote_addr):
    logs.logV(user, 'ReportsManager.select_reports("'+user+'","'+ remote_addr+'")')
    return reportsDAO.select_reports(user, True)

def select_report(user, remote_addr, id):
    logs.logV(user, 'ReportsManager.select_report("'+user+'","'+ remote_addr+'",'+ str(id) +')')
    return reportsDAO.select_report(user, id)
	

def testing():
    #create_report('user1', '127.0.0.1', 'id0001', 'El paciente presenta el abdomen distendido.', 0)
    create_report('user1', '127.0.0.1', 'id0001', 'Se observan calcificaciones dispersas en la aorta y en sus principales ramas, compatibles con la aterosclerosis.', 1)
    #text = 'el paciente presenta el abdomen distendido.'
    #text_pre = nlputils.preprocessDoc(text)
    #embedding = nlputils.getembedding(text_pre)
    #print(embedding)
    #embedding_ser = utils.serialiceNumpyArray(embedding)
    #print(embedding_ser)
    #embedding_deser = utils.deserialiceNumpyArray(embedding_ser)
    #print(embedding_deser)
    #print(nlputils.calculateCosineSimilarity(embedding, embedding_deser))

#testing()
