'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''
from datetime import datetime
import logging
import logging.handlers

import com.fmedinafernandez.ClinicalNELEngine.general.configuration as configuration


STANDARD_LOG_PATH = configuration.PATH_TRABAJO+"\\"+"trazaStandard.log"
LOPD_LOG_PATH = configuration.PATH_TRABAJO+"\\"+"trazaLOPD.log"
STANDARD_LOG_PATH_2 = configuration.PATH_TRABAJO+"\\"+"trazaStandard2.log"
LOPD_LOG_PATH_2 = configuration.PATH_TRABAJO+"\\"+"trazaLOPD2.log"
MAX_LOG_FILE_SIZE = 10*1048576 #Mbytes
MAX_BACKUP_COUNT = 100

loggerStandard = logging.getLogger('CLINICALNELENGINE')
loggerStandard.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handlerStandard = logging.handlers.RotatingFileHandler(STANDARD_LOG_PATH, maxBytes=MAX_LOG_FILE_SIZE, backupCount=MAX_BACKUP_COUNT)
loggerStandard.addHandler(handlerStandard)
# Add the formatter to the handler
formatterStandard = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handlerStandard.setFormatter(formatterStandard)

loggerLOPD = logging.getLogger('CLINICALNELENGINE_LOPD')
loggerLOPD.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handlerLOPD = logging.handlers.RotatingFileHandler(LOPD_LOG_PATH, maxBytes=MAX_LOG_FILE_SIZE)
loggerLOPD.addHandler(handlerLOPD)
# Add the formatter to the handler
formatterLOPD = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handlerLOPD.setFormatter(formatterLOPD)

loggerStandard2 = logging.getLogger('CLINICALNELENGINE')
loggerStandard2.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handlerStandard2 = logging.handlers.RotatingFileHandler(STANDARD_LOG_PATH_2, maxBytes=MAX_LOG_FILE_SIZE, backupCount=MAX_BACKUP_COUNT)
loggerStandard2.addHandler(handlerStandard2)
# Add the formatter to the handler
formatterStandard2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handlerStandard2.setFormatter(formatterStandard2)

loggerLOPD2 = logging.getLogger('CLINICALNELENGINE_LOPD')
loggerLOPD2.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handlerLOPD2 = logging.handlers.RotatingFileHandler(LOPD_LOG_PATH_2, maxBytes=MAX_LOG_FILE_SIZE)
loggerLOPD2.addHandler(handlerLOPD2)
# Add the formatter to the handler
formatterLOPD2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handlerLOPD2.setFormatter(formatterLOPD2)

#Timestamp-User-Source IP-Action Type-Object-Patient nhc/study uid...
def logLOPD(user, remote_addr, lopd_op, lopd_result, message=None):
    text = user + '-' + remote_addr + '-' + lopd_op + '-' + lopd_result
    if message is not None:
        text = text + '-' + message;
        
    try:
        loggerLOPD.info(text)
    except:
        try:
            loggerLOPD2.info(text)
        except:
            print('No ha sido posible generar traza', text)

def log(cadena):
    try:
        loggerStandard.info(cadena)
    except:
        try:
            loggerStandard2.info(cadena)
        except:
            print('No ha sido posible generar traza:', cadena)

def logV(usuario, cadena):
    log(usuario + "-" + cadena)    
   
