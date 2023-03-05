'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''

import os
import com.fmedinafernandez.ClinicalNELEngine.database.TerminosClinicosDAO as terminosclinicosdao
import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
import com.fmedinafernandez.ClinicalNELEngine.general.utils as utils
import com.fmedinafernandez.ClinicalNELEngine.general.NLPutils as nlputils
import com.fmedinafernandez.ClinicalNELEngine.general.exceptions as exceptions
import com.fmedinafernandez.ClinicalNELEngine.general.configuration as configuration

def select_terminoclinico(user,remote_addr, id):
    logs.logV(user, 'terminoclinicosManager.select_terminoclinico("'+user+'","'+remote_addr+','+str(id)+')')
    result = []
    result.append(terminosclinicosdao.select_terminoclinico(id))
    return result

def select_terminoclinico_by_id(user,remote_addr, id):
    logs.logV(user, 'terminoclinicosManager.select_terminoclinico_by_id("'+user+'","'+remote_addr+','+str(id)+')')
    result = []
    result.append(terminosclinicosdao.select_terminoclinico_by_id(id))
    return result
	
def select_terminosclinicos(user, remote_addr, id='', termino='', num_palabras=0):
    logs.log('terminoclinicosManager.select_terminosclinicos('+user+','+remote_addr+','+id+','+termino+','+str(num_palabras)+")")
	
    if id != '':
        return select_terminoclinico(user,remote_addr, id)

    if termino != '':
        return terminosclinicosdao.select_terminosclinicos(termino)

    if num_palabras != 0:
        return terminosclinicosdao.select_terminosclinicos_por_palabras(num_palabras)
		
    return terminosclinicosdao.select_terminosclinicos()

def create_terminoclinico(user, remote_addr, idtermino, termino):
    logs.logV(user, 'terminoclinicosManager.create_terminoclinico('+user+','+remote_addr+','+str(idtermino)+','+str(termino)+')')
    preprocessed_term = nlputils.preprocessDoc(termino)
    if preprocessed_term == "":
        preprocessed_term = termino
    num_palabras = len(preprocessed_term.split(" "))
    return terminosclinicosdao.create_terminoclinico(idtermino, termino, num_palabras, utils.serialiceNumpyArray(nlputils.getembedding(preprocessed_term)))

def update_terminoclinico(user, remote_addr, idtermino, termino):
    logs.logV(user, 'terminoclinicosManager.update_terminoclinico('+user+','+remote_addr+','+str(idtermino)+','+str(termino)+')')
    preprocessed_term = nlputils.preprocessDoc(termino)
    if preprocessed_term == "":
        preprocessed_term = termino
    num_palabras = len(preprocessed_term.split(" "))
    return terminosclinicosdao.update_terminoclinico(idtermino, termino, num_palabras, utils.serialiceNumpyArray(nlputils.getembedding(preprocessed_term)))

def delete_terminoclinico(user, remote_addr, id):
    logs.logV(user,'terminoclinicosManager.delete_terminoclinico('+user+','+remote_addr+','+str(id) + ')')
    return terminosclinicosdao.delete_terminoclinico(id)

def load_terminosclinicos(user, remote_addr):
    logs.logV(user,'terminoclinicosManager.load_terminosclinicos('+user+','+remote_addr+')')

    terminosclinicosdao.delete_terminosclinicos()
	
    f = open('com\\fmedinafernandez\\ClinicalNELEngine\\data\\der2_Refset_ProblemasSaludAHSpainExtensionSnapshot_ES_20221201.txt', 'r', encoding='utf-8')
    first_item = True
    for row in f:
        if first_item:
            first_item = False
            continue
        values = row.strip().split("\t")
        #id	effectiveTime	active	moduleId	refsetId	referencedComponentId	term
        #print(values)
        termino = {}
        termino["id"] = values[0];
        termino["effectiveTime"] = values[1];
        termino["active"] = values[2];
        termino["moduleId"] = values[3];
        termino["refsetId"] = values[4];
        termino["referencedComponentId"] = values[5];
        termino["term"] = values[6];
        #print(termino)
        preprocessed_term = nlputils.preprocessDoc(termino["term"])
		
		#En caso de que no sea posible el preprocesado, dejamos el valor inicial
        if preprocessed_term == "":
            preprocessed_term = termino["term"]

        #Se almacena el número de palabras del texto preprocesado
        termino["num_palabras"] = len(termino["term"].split(" "));

        embedding_FastText = utils.serialiceNumpyArray(nlputils.getembedding(preprocessed_term))
        #embedding_Transformer = utils.serialiceNumpyArray(nlputils.getembedding_Transformer(preprocessed_term))
        
        embedding_Transformer = ''

        terminosclinicosdao.create_terminoclinico(termino["id"],termino["term"],termino["num_palabras"],embedding_FastText,embedding_Transformer)

    f.close();	

    return True
	

	
def testing():
    load_terminosclinicos('user1', '127.0.0.1')    


#testing()
	

