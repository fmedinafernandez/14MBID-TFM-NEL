'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''

import datetime
import mysql.connector
from mysql.connector import errorcode

import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
import com.fmedinafernandez.ClinicalNELEngine.general.configuration as configuration
import com.fmedinafernandez.ClinicalNELEngine.database.TerminosClinicosDAO as terminosclinicosdao

def create_report(name, owner, idreport, reportbody):
    logs.log('ReportsDAO.create_report('+name+','+owner+','+str(idreport)+','+str(reportbody)+')')

    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)

        cursor = cnx.cursor()
        
        add_report = ("INSERT INTO reports "
                 "(creation_datetime, last_update_datetime, name, owner, idreport, reportbody) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        data_report = (datetime.datetime.now(), datetime.datetime.now(), name, owner, idreport, reportbody)
        cursor.execute(add_report, data_report)
        
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

def select_reports(owner, all_owners=False):
    logs.log('ReportsDAO.select_reports('+owner+','+str(all_owners)+')')
    lista_reports = []
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        query = ("SELECT r.id, r.creation_datetime, r.last_update_datetime, r.name, r.owner, r.idreport, r.reportbody "
            "FROM reports r " )
        
        if not all_owners:
            query += ("WHERE r.owner='" + owner + "' ") 

        query += ("ORDER BY r.id ASC") 
            
        #logs.log(query)
        cursor.execute(query)
        for (id, creation_datetime, last_update_datetime, name, owner, idreport, reportbody) in cursor:
            #logs.log(str(id) +","+name+","+status+","+owner+","+str(idreport)+","+str(reportbody))
            report = {'id':'', 'creation_datetime':'', 'last_update_datetime':'', 'name':'', 'owner':'', 'idreport':'', 'reportbody':''}
            report['id']=id
            report['creation_datetime']=creation_datetime
            report['last_update_datetime']=last_update_datetime
            report['name']=name
            report['owner']=owner
            report['idreport']=idreport
            report['reportbody']=reportbody
            lista_reports.append(report)
    
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
        return lista_reports
    else:
        cnx.close()
        return lista_reports

def select_report(owner, id):
    logs.log('ReportsDAO.select_report('+owner+','+str(id) + ')')
    report = {'id':'', 'name':'', 'status':'', 'owner':'', 'idreport':'', 'reportbody':''}
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        
        query = ("SELECT r.id, r.creation_datetime, r.last_update_datetime, r.name, r.owner, r.idreport, r.reportbody  "
                 "FROM reports r "
                 "WHERE r.id=" + str(id) + " AND r.owner='" + owner + "'")
        #logs.log(query)
        cursor.execute(query)
        for (id, creation_datetime, last_update_datetime, name, owner, idreport, reportbody) in cursor:
            #logs.log(str(id) +","+name+","+status+","+owner+","+str(idreport)+","+str(reportbody))
            report = {'id':'', 'creation_datetime':'', 'last_update_datetime':'', 'name':'', 'owner':'', 'idreport':'', 'reportbody':''}
            report['id']=id
            report['creation_datetime']=creation_datetime
            report['last_update_datetime']=last_update_datetime
            report['name']=name
            report['owner']=owner
            report['idreport']=idreport
            report['reportbody']=reportbody
        
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
        return report
    else:
        cnx.close()
        return report

def get_reports(owner, all_owners, idreport, owner2, termino):
    logs.log('ReportsDAO.get_reports('+owner+','+str(all_owners)+','+idreport+','+owner2+','+termino+')')
    lista_reports = []
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        query = ("SELECT DISTINCT r.id, r.creation_datetime, r.last_update_datetime, r.name, r.owner, r.idreport, r.reportbody "
            "FROM reports r, terminosclinicos_report tr  " 
			"WHERE r.id = tr.report_id " )
        
        if not all_owners:
            query += ("AND r.owner='" + owner + "' ") 
        if idreport != '':
            query += ("AND r.idreport='" + idreport + "' ") 
        if owner2 != '':
            query += ("AND r.owner='" + owner2 + "' ") 
        if termino != '':
            #query += ("AND tr.termino LIKE '%" + termino + "%' ")
            query += ("AND r.id IN(SELECT DISTINCT report_id FROM terminosclinicos_report WHERE termino LIKE '%" + termino + "%')")
            

        query += ("ORDER BY r.id ASC") 
            
        #logs.log(query)
        cursor.execute(query)
        max_num_registros = 200
        for (id, creation_datetime, last_update_datetime, name, owner, idreport, reportbody) in cursor:
            #logs.log(str(id) +","+name+","+status+","+owner+","+str(idreport)+","+str(reportbody))
            report = {'id':'', 'creation_datetime':'', 'last_update_datetime':'', 'name':'', 'owner':'', 'idreport':'', 'reportbody':''}
            report['id']=id
            report['creation_datetime']=creation_datetime
            report['last_update_datetime']=last_update_datetime
            report['name']=name
            report['owner']=owner
            report['idreport']=idreport
            report['reportbody']=reportbody
            lista_reports.append(report)
            max_num_registros = max_num_registros - 1
            if max_num_registros == 0:
                break;
    
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
        return lista_reports
    else:
        cnx.close()
        return lista_reports

def get_reports_and_labels(owner, all_owners, idreport, owner2, termino):
    logs.log('ReportsDAO.get_reports_and_labels('+owner+','+str(all_owners)+','+idreport+','+owner2+','+termino+')')
    lista_reports = []
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        query = ("SELECT r.id, r.creation_datetime, r.last_update_datetime, r.name, r.owner, r.idreport, r.reportbody, tr.source_text, tr.idtermino, tr.termino, tr.cosine_similarity, tr.model "
            "FROM reports r, terminosclinicos_report tr  " 
			"WHERE r.id = tr.report_id " )
        
        if not all_owners:
            query += ("AND r.owner='" + owner + "' ") 
        if idreport != '':
            query += ("AND r.idreport='" + idreport + "' ") 
        if owner2 != '':
            query += ("AND r.owner='" + owner2 + "' ") 
        if termino != '':
            #query += ("AND tr.termino LIKE '%" + termino + "%' ")
            query += ("AND r.id IN(SELECT DISTINCT report_id FROM terminosclinicos_report WHERE termino LIKE '%" + termino + "%')")
            

        query += ("ORDER BY r.id ASC") 
            
        #logs.log(query)
        cursor.execute(query)
        max_num_registros = 200
        for (id, creation_datetime, last_update_datetime, name, owner, idreport, reportbody, source_text, idtermino, termino, cosine_similarity, model) in cursor:
            #logs.log(str(id) +","+name+","+status+","+owner+","+str(idreport)+","+str(reportbody))
            report = {'id':'', 'creation_datetime':'', 'last_update_datetime':'', 'name':'', 'owner':'', 'idreport':'', 'reportbody':'', 'source_text':'', 'idtermino':'', 'termino':'', 'cosine_similarity':'', 'model':''}
            report['id']=id
            report['creation_datetime']=creation_datetime
            report['last_update_datetime']=last_update_datetime
            report['name']=name
            report['owner']=owner
            report['idreport']=idreport
            report['reportbody']=reportbody
            report['source_text']=source_text
            report['idtermino']=idtermino
            report['termino']=termino
            report['cosine_similarity']=cosine_similarity
            report['model']=model
            lista_reports.append(report)
            max_num_registros = max_num_registros - 1
            if max_num_registros == 0:
                break;
    
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
        return lista_reports
    else:
        cnx.close()
        return lista_reports

		
		
def update_report(owner, id, idreport, reportbody):
    logs.log('ReportsDAO.update_report('+owner+','+str(id)+','+str(idreport) + ','+str(reportbody)+')')
    report = {'id':'', 'name':'', 'owner':'', 'idreport':'', 'reportbody':''}
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        
        update_report = ("UPDATE reports "
                      "SET idreport='" + str(idreport) + "' "
					  ", reportbody='" + str(reportbody) + "' "
                      ",last_update_datetime='" + str(datetime.datetime.now()) + "' "
                      "WHERE id=" + str(id) + " AND owner='" + owner + "'")
            
        logs.log(update_report)
        cursor.execute(update_report)
        
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

def delete_report(owner, reportid):
    logs.log('ReportsDAO.delete_report('+owner+','+str(reportid) + ')')
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        
        delete_report = ("DELETE FROM reports WHERE id=" + str(reportid) + " AND owner='" + owner + "'")
        
        #logs.log(query)
        cursor.execute(delete_report)
        
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

def create_termino_report(report_id, source_text, idtermino, cosine_similarity, model):
    logs.log('ReportsDAO.create_termino_report('+str(report_id)+','+str(source_text)+','+str(idtermino)+','+str(cosine_similarity)+','+str(model)+')')

    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)

        cursor = cnx.cursor()
        
        add_item = ("INSERT INTO terminosclinicos_report "
                 "(report_id, source_text, idtermino, termino, cosine_similarity, model) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        data_item = (report_id, source_text, idtermino, terminosclinicosdao.select_terminoclinico(idtermino)['termino'], float(cosine_similarity), model)
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
		
def select_termino_reports(report_id):
    logs.log('ReportsDAO.select_termino_reports('+str(report_id)+')')
    lista_items = []
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        query = ("SELECT tr.id, tr.report_id, tr.source_text, tr.idtermino, tr.termino, tr.cosine_similarity, tr.model "
            "FROM terminosclinicos_report tr  " 
			"WHERE tr.report_id = " + str(report_id) + " ")
        
        query += ("ORDER BY tr.id ASC") 
            
        #logs.log(query)
        cursor.execute(query)
        for (id, report_id, source_text, idtermino, termino, cosine_similarity, model) in cursor:
            #logs.log(str(id) +","+str(report_id)+","+idtermino+","+termino)
            report = {'id':'', 'report_id':'', 'source_text':'', 'idtermino':'', 'termino':'', 'cosine_similarity':'', 'model':''}
            report['id']=id
            report['source_text']=source_text
            report['report_id']=report_id
            report['idtermino']=idtermino
            report['termino']=termino
            report['cosine_similarity']=cosine_similarity
            report['model']=model
            lista_items.append(report)
    
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
		
def delete_termino_reports(report_id):
    logs.log('ReportsDAO.delete_termino_reports('+str(report_id) + ')')
    try:
        cnx = mysql.connector.connect(user=configuration.CLINICALNELENGINEDB_USER, password=configuration.CLINICALNELENGINEDB_PASS, database=configuration.CLINICALNELENGINEDB_DATABASE)
        cursor = cnx.cursor()
        
        delete_item = ("DELETE FROM terminosclinicos_report WHERE report_id=" + str(report_id))
        
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
    create_report('name1', 'owner1', 'id0001', 'Este un texto de ejemplo')
    print("<->")
    items = select_reports('owner1')
    for item in items:
        print( item )
    print("<->")
    print(select_report('owner1',1))
    print("<->")
    update_report('owner1',1, 'id0001u', 'Este es un texto de ejemplo modificado')
    print(select_report('owner1',1))
    print("<->")
    delete_report('owner1',2)    
    print(select_report('owner1',2))
    print("<->")
    delete_termino_reports(1)
    create_termino_report(1, 2)
#testing()
