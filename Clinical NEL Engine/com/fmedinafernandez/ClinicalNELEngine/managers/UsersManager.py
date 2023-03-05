'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''

import com.fmedinafernandez.ClinicalNELEngine.general.ldap as ldap
import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
import com.fmedinafernandez.ClinicalNELEngine.general.constants as constants



def validateUser(user, password, remote_addr):
    logs.logV(user,'UsersManager.validateUser("'+user+'",*******,"'+remote_addr+'")')
    try:
        #exists = ldap.valida_Usuario(user,password)
        #Auto-validation
        exists = True
    except:
        logs.logV(user,'UsersManager.validateUser().User validation error.')
        logs.logLOPD(user, remote_addr, constants.USER_VALIDATION_LOPD_OP, constants.ERROR_OP)
        raise
    else:
        if exists:
            logs.logLOPD(user, remote_addr, constants.USER_VALIDATION_LOPD_OP, constants.CORRECT_OP)
        else:    
            logs.logLOPD(user, remote_addr, constants.USER_VALIDATION_LOPD_OP, constants.INCORRECT_OP)
        return exists
    
