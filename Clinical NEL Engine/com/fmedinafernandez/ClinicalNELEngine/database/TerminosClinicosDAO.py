'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''

import datetime
import mysql.connector
from mysql.connector import errorcode

import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
import com.fmedinafernandez.ClinicalNELEngine.general.configuration as configuration


def create_terminoclinico(idtermino, termino, num_palabras, embedding, embedding2=''):
    logs.log('TerminosClinicosDAO.create_terminoclinico('+str(idtermino)+','+str(termino)+','+str(num_palabras)+',EMBEDDING)')
    id = 0
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)

        cursor = cnx.cursor()
        
        add_item = ("INSERT INTO terminosclinicos "
                 "(idtermino, termino, num_palabras, embedding, embedding2) "
                 "VALUES (%s, %s, %s, %s, %s)")
        data_item = (idtermino, termino, num_palabras, embedding, embedding2)
        cursor.execute(add_item, data_item)
        
        cnx.commit()
        id = cursor.lastrowid
        cursor.close()
        cnx.close()
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return id
    else:
        cnx.close()
        return id

		
def select_terminosclinicos(termino=''):
    logs.log('TerminosClinicosDAO.select_terminosclinicos('+termino+')')
    lista_items = []
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        query = ("SELECT tc.id, tc.idtermino, tc.termino, tc.num_palabras, tc.embedding, tc.embedding2 "
            "FROM terminosclinicos tc ")
        if termino != "":
            query += ("WHERE tc.termino LIKE '%" + termino + "%' ")
        
        query += ("ORDER BY tc.id ASC") 
            
        #logs.log(query)
        cursor.execute(query)
        for (id, idtermino, termino, num_palabras, embedding, embedding2) in cursor:
            #logs.log(str(id)+","+str(idtermino)+","+str(termino)+","+str(embedding))
            item = {'id':'', 'idtermino':'', 'termino':'', 'num_palabras':'', 'embedding':'', 'embedding2':''}
            item['id']=id
            item['idtermino']=idtermino
            item['termino']=termino
            item['num_palabras']=num_palabras
            item['embedding']=embedding
            item['embedding2']=embedding2
            lista_items.append(item)
    
        cursor.close()
        cnx.commit()
        cnx.close()
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return lista_items
    else:
        cnx.close()
        return lista_items

def select_terminosclinicos_por_palabras(num_palabras=0):
    logs.log('TerminosClinicosDAO.select_terminosclinicos_por_palabras('+str(num_palabras)+')')
    lista_items = []
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        query = ("SELECT tc.id, tc.idtermino, tc.termino, tc.num_palabras, tc.embedding, tc.embedding2 "
            "FROM terminosclinicos tc ")
        if num_palabras > 0:
            query += ("WHERE tc.num_palabras = " + num_palabras + " ")
        
        query += ("ORDER BY tc.id ASC") 
            
        #logs.log(query)
        cursor.execute(query)
        for (id, idtermino, termino, num_palabras, embedding, embedding2) in cursor:
            #logs.log(str(id)+","+str(idtermino)+","+str(termino)+","+str(embedding))
            item = {'id':'', 'idtermino':'', 'termino':'', 'num_palabras':'', 'embedding':'', 'embedding2':''}
            item['id']=id
            item['idtermino']=idtermino
            item['termino']=termino
            item['num_palabras']=num_palabras
            item['embedding']=embedding
            item['embedding2']=embedding2
            lista_items.append(item)
    
        cursor.close()
        cnx.commit()
        cnx.close()
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return lista_items
    else:
        cnx.close()
        return lista_items
		
def select_terminoclinico(idtermino):
    logs.log('TerminosClinicosDAO.select_terminoclinico('+str(idtermino) + ')')
    item = {'id':'', 'idtermino':'', 'termino':'', 'embedding':''}
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        
        query = ("SELECT tc.id, tc.idtermino, tc.termino, tc.num_palabras, tc.embedding, tc.embedding2 "
			"FROM terminosclinicos tc "
			"WHERE tc.idtermino='" + str(idtermino) + "' ")

        query += ("ORDER BY tc.id ASC") 
			
         #logs.log(query)
        cursor.execute(query)
        for (id, idtermino, termino, num_palabras, embedding, embedding2) in cursor:
            #logs.log(str(id)+","+str(idtermino)+","+str(termino))
            item = {'id':'', 'idtermino':'', 'termino':'', 'num_palabras':'', 'embedding':'', 'embedding2':''}
            item['id']=id
            item['idtermino']=idtermino
            item['termino']=termino
            item['num_palabras']=num_palabras
            item['embedding']=embedding
            item['embedding2']=embedding2
        
        cursor.close()
        cnx.commit()
        cnx.close()
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return item
    else:
        cnx.close()
        return item

def select_terminoclinico_by_id(idtermino):
    logs.log('TerminosClinicosDAO.select_terminoclinico_by_id('+str(idtermino) + ')')
    item = {'id':'', 'idtermino':'', 'termino':'', 'embedding':''}
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        
        query = ("SELECT tc.id, tc.idtermino, tc.termino, tc.num_palabras, tc.embedding, tc.embedding2 "
			"FROM terminosclinicos tc "
			"WHERE tc.id=" + str(idtermino) + " ")

        query += ("ORDER BY tc.id ASC") 
			
         #logs.log(query)
        cursor.execute(query)
        for (id, idtermino, termino, num_palabras, embedding, embedding2) in cursor:
            #logs.log(str(id)+","+str(idtermino)+","+str(termino))
            item = {'id':'', 'idtermino':'', 'termino':'', 'num_palabras':'', 'embedding':'', 'embedding2':''}
            item['id']=id
            item['idtermino']=idtermino
            item['termino']=termino
            item['num_palabras']=num_palabras
            item['embedding']=embedding
            item['embedding2']=embedding2
        
        cursor.close()
        cnx.commit()
        cnx.close()
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return item
    else:
        cnx.close()
        return item


		
def update_terminoclinico(id, idtermino, termino, num_palabras, embedding, embedding2):
    logs.log('TerminosClinicosDAO.update_terminoclinico('+str(id)+','+str(idtermino) + ','+str(termino) + ','+str(num_palabras) + ',EMBEDDING)')
    item = {'id':'', 'idtermino':'', 'termino':'', 'num_palabras':'', 'embedding':'', 'embedding2':''}
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        
        update_job = ("UPDATE terminosclinicos "
                      "SET idtermino='" + str(idtermino) + "' "
                      ",termino='" + str(termino) + "' "
                      ",num_palabras='" + str(num_palabras) + "' "
                      ",embedding='" + str(embedding) + "' "
                      ",embedding2='" + str(embedding2) + "' "
                      "WHERE id=" + str(id))
            
        logs.log(update_job)
        cursor.execute(update_job)
        
        cursor.close()
        cnx.commit()
        cnx.close()
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return False
    else:
        cnx.close()
        return True

def delete_terminoclinico(id):
    logs.log('TerminosClinicosDAO.delete_terminoclinico('+str(id) + ')')
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        
        delete_item = ("DELETE FROM terminosclinicos WHERE id=" + str(id) )
        
        #logs.log(query)
        cursor.execute(delete_item)
        
        cursor.close()
        cnx.commit()
        cnx.close()
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

def delete_terminosclinicos():
    logs.log('TerminosClinicosDAO.delete_terminosclinicos()')
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        
        delete_item = ("DELETE FROM terminosclinicos ")
        
        #logs.log(query)
        cursor.execute(delete_item)
        
        cursor.close()
        cnx.commit()
        cnx.close()
      
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

def testing():		
    create_terminoclinico('1', 'TERM', 1, 'EMBEDDING', 'EMBEDDING')
    print("<->")
    lista_items = select_terminosclinicos()
    for item in lista_items:
        print(item)
    print("<->")
    print(select_terminoclinico(1))
    print("<->")
    update_terminoclinico(1, '2', 'TERM2', 1, 'EMBEDDING2', 'EMBEDDING2')
    print("<->")
    lista_items = select_terminosclinicos()
    for item in lista_items:
        print(item)
    print("<->")
    delete_terminoclinico(1)
    lista_items = select_terminosclinicos()
    for item in lista_items:
        print(item)
    print("<->")
    delete_terminosclinicos()
#testing()
