'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''

import com.fmedinafernandez.ClinicalNELEngine.database.JobsDAO as jobsdao
import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
import com.fmedinafernandez.ClinicalNELEngine.general.utils as utils
import com.fmedinafernandez.ClinicalNELEngine.general.exceptions as exceptions
import com.fmedinafernandez.ClinicalNELEngine.general.configuration as configuration
import com.fmedinafernandez.ClinicalNELEngine.managers.StudiesManager as studiesmanager

JOBTYPE_REPORT_MULTILABEL_CLASSIFICATION = jobsdao.JOBTYPE_REPORT_MULTILABEL_CLASSIFICATION



def select_job(user,remote_addr, owner, job_id):
    logs.logV(user, 'JobsManager.select_job("'+user+'","'+remote_addr+'",'+owner+','+str(job_id)+')')
    return jobsdao.select_job(owner,job_id)

def select_jobs(user, remote_addr, owner, skip_ended=True, all_owners=False):
    logs.log('JobsManager.select_jobs('+user+','+remote_addr+','+owner+','+str(skip_ended)+','+str(all_owners)+')')
    return jobsdao.select_jobs(owner, skip_ended, all_owners)

def create_job(user, remote_addr, name, owner, report_id, strategy_id, comments):
    logs.logV(user, 'JobsManager.create_job('+user+','+remote_addr+','+name+','+owner+','+str(report_id)+','+str(strategy_id)+','+comments+')')
    return jobsdao.create_job(name, owner, report_id, strategy_id, comments)

def delete_job(user, remote_addr, owner, jobid):
    logs.logV(user,'JobsManager.delete_job('+user+','+remote_addr+','+owner+','+str(jobid) + ')')
    return jobsdao.delete_job(owner, jobid)

def execute_job_label_report(user, remote_addr, owner, jobid):
    logs.logV(user,'JobsManager.execute_job_label_report('+user+','+remote_addr+','+owner+','+str(jobid) + ')')
    
    
    job=jobsdao.select_job(owner,jobid)
    if job.get('id') is None:
        raise
    
    # Get data from fields
    usuario=job['owner']
    informeOrigen = job['report_id']
    estrategia = job['strategy_id']
	
	#MODIFICAR CON LA LÓGICA
    try:
		#Modificación de campos DICOM
		jobsdao.update_job_status(owner, jobid, jobsdao.JOBSTATUS_STUDY_MODIFYING, '')
		#nuevoStudyInstanceUID = studiesmanager.modify_study(usuario, nhcDestino, hospitaldestino, studyinstanceuid, directory, True)
		jobsdao.update_job_status(owner, jobid, jobsdao.JOBSTATUS_STUDY_MODIFIED, '')
		
		#Modificado correcto - Eliminamos los ficheros .bak
		utils.delete_bak_files(directory)
				
	except exceptions.DCMTKError as e:
		logs.logV(usuario,'Duplicado de estudios. Error al modificar el estudio. modificadoIncorrecto ({0}): {1}'.format(e.expression, e.message))
		#En este caso no eliminamos el directorio, para analizar posteriormente
		jobsdao.update_job_status(owner, jobid, jobsdao.JOBSTATUS_JOB_ERROR, 'Error al modificar el estudio')
	except:
		logs.logV(usuario,'Duplicado de estudios. Error al modificar el estudio. modificadoIncorrecto')
		#En este caso no eliminamos el directorio, para analizar posteriormente
		jobsdao.update_job_status(usuario, jobid, jobsdao.JOBSTATUS_JOB_ERROR, 'Error al modificar el estudio')



def execute_job(user, remote_addr, owner, jobid):
    logs.logV(user,'JobsManager.execute_job('+user+','+remote_addr+','+owner+','+str(jobid) + ')')
    
    
    job=jobsdao.select_job(owner,jobid)
    if job.get('id') is None:
        raise
    jobsdao.update_job_status(owner,jobid,jobsdao.JOBSTATUS_JOB_CREATED)
    
def execute_pending_jobs(limit=10):
    logs.logV('system','JobsManager.execute_pending_jobs("'+str(limit)+'")')

    counter = 0    
    jobs=jobsdao.select_jobs('system',True,True)
    for job in jobs:
        #Execute only created and error jobs
        #logs.logV('system',str(job.get('id')) + "-" + job.get('status'))
        if job.get('status') == "JOB_CREATED":
            if job.get('name') == jobsdao.JOBTYPE_REPORT_MULTILABEL_CLASSIFICATION:
                try:
                    execute_job_label_report('system', configuration.REST_SERVER_HOST, job.get('owner'), job.get('id'))
                except:
                    #Follow executing jobs
                    None
            else:
                raise
            counter = counter + 1
            if counter == limit:
                break 