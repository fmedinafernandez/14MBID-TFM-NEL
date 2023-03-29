'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''

CLINICALNELENGINE_VERSION = '1.0.230328'
CLINICALNELENGINE_DATE_VERSION ='28/03/2023'

#ConfiguraciÃƒÂ³n 


#Constantes
PATH_TRABAJO='.'

VALIDATE_USER = True #By default set it to True!!!
#LDAP_SERVER_URL='ldap://10.116.2.120:1389' #Test environment
LDAP_SERVER_URL='ldap://10.154.208.6:1389' #Production environment

CLINICALNELENGINEDB_USER = 'clinicalneluser'
CLINICALNELENGINEDB_PASS = 'clinicalnelpass'
CLINICALNELENGINEDB_DATABASE = 'clinicalneldb'

COSINE_SIMILARITY_PERCENTAGE_THRESHOLD = 0.9

REST_SERVER_SSL = False
#REST_SERVER_HOST = '10.116.144.134'
#REST_SERVER_HOST = '10.116.82.10'
REST_SERVER_HOST = '127.0.0.1'
REST_SERVER_PORT = 5003

SSL_CERTIFICATE_CERT = '.\certificate\cacert.pem'
SSL_CERTIFICATE_KEY = '.\certificate\cakey.pem'
SSL_CERTIFICATE_PASSWORD = 'prueba'

CRYPTO_SECRET_KEY = 'something_super_secret_change_in_production'
CRYPTO_TOKEN_EXPIRATION = 3600 #One hour fo expiration time







