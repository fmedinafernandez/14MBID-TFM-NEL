'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''
#pip install ldap3
from ldap3 import Server, Connection, ALL

import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
import com.fmedinafernandez.ClinicalNELEngine.general.configuration as configuration

def valida_Usuario(usuario, contrasena):
    logs.logV(usuario,'ldap.valida_Usuario("'+usuario+'","*********")')
    
    if  not configuration.VALIDATE_USER:
        return True
    
    existe = False
    try:
        server = Server(configuration.LDAP_SERVER_URL, get_info=ALL)
        conn = Connection(server, 'uid='+usuario+',ou=personales,ou=usuarios,o=corp', contrasena, auto_bind=True)
        existe = conn.search('uid='+usuario+',ou=personales,ou=usuarios,o=corp', '(objectclass=person)')
        conn.unbind()
    #except LDAPException as e:
    #    logs.logV(usuario,'Validación de usuario. Error al validar el usuario. validacionIncorrecta:', str(e))
    #    raise
    except:
        logs.logV(usuario,'ldap.Validación de usuario. Error al validar el usuario. validacionIncorrecta')
        raise
    else:
        return existe   
    
