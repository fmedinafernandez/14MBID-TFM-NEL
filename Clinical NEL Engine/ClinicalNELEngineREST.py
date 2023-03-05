'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''


#https://www.codementor.io/sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
#pip install flask flask-jsonpify flask-sqlalchemy flask-restful flask_httpauth

#https://flask.palletsprojects.com/en/2.2.x/errorhandling/#error-logging-tools
#pip install sentry-sdk[flask]

from flask import Flask, request, make_response
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
import ssl

import com.fmedinafernandez.ClinicalNELEngine.general.exceptions as exceptions
import com.fmedinafernandez.ClinicalNELEngine.general.configuration as configuration
import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs
import com.fmedinafernandez.ClinicalNELEngine.general.crypto as crypto
import com.fmedinafernandez.ClinicalNELEngine.managers.UsersManager as usersmanager
import com.fmedinafernandez.ClinicalNELEngine.managers.ReportsManager as reportsmanager
import com.fmedinafernandez.ClinicalNELEngine.managers.TerminosClinicosManager as terminosclinicosmanager

#import sentry_sdk
#from sentry_sdk.integrations.flask import FlaskIntegration

#sentry_sdk.init('YOUR_DSN_HERE', integrations=[FlaskIntegration()])



#db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

#pip install flask_cors
from flask_cors import CORS
CORS(app, origins="http://localhost:8000", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials", "user", "password", "token", "id", "idtermino", "termino", "idreport", "reportid", "model", "owner"],
    supports_credentials=True, intercept_exceptions=False)


class Application(Resource):

    #GET Application : Info. de version de la aplicacion
    def get(self):
        user = request.headers.get('user')
        remote_addr = request.remote_addr
        logs.log(user + ' - ' + remote_addr + '- Application.get()')
        
        result = {'result':'success', 'data':{'version':configuration.CLINICALNELENGINE_VERSION, 'date':configuration.CLINICALNELENGINE_DATE_VERSION}}
        return jsonify(result)

class TerminosClinicos(Resource):

	#PUT terminosclinicos : Carga de término en la aplicacion
    def put(self):
        user = request.headers.get('user')
        remote_addr = request.remote_addr
        logs.log(user + ' - ' + remote_addr + '- TerminosClinicos.put()')
        
        args = request.headers
        if args.get('user') is not None and args.get('token') is not None and args.get('idtermino') is not None and args.get('termino') is not None:
            user = args['user']
            token = args['token']
            idtermino = args['idtermino']
            termino = args['termino'] 
            login = crypto.verify_auth_token(token)
            if login is None or login != user:
                result = {'result': 'error', 'message': 'Invalid token'}
                #return jsonify(result)

            id = terminosclinicosmanager.create_terminoclinico(user,remote_addr,idtermino,termino)
            termino = terminosclinicosmanager.select_terminoclinico_by_id(user,remote_addr, id)
            result = {'result': termino, 'message': 'Registro creado'}
            return jsonify(result)
        else:
            result = {'result': 'error', 'message': 'Parametros incorrectos'}
            return jsonify(result)

	#POST terminosclinicos : Carga de términos en la aplicacion
    def post(self):
        user = request.headers.get('user')
        remote_addr = request.remote_addr
        logs.log(user + ' - ' + remote_addr + '- TerminosClinicos.post()')
        
        args = request.headers
        if args.get('user') is not None and args.get('token') is not None:
            user = args['user']
            token = args['token']
            login = crypto.verify_auth_token(token)
            if login is None or login != user:
                result = {'result': 'error', 'message': 'Invalid token'}
                #return jsonify(result)

            terminosclinicosmanager.load_terminosclinicos(user,remote_addr)
        else:
            result = {'result': 'error', 'message': 'Parametros incorrectos'}
            return jsonify(result)

    #GET terminosclinicos : Info. de version de la aplicacion
    def get(self):
        user = request.headers.get('user')
        remote_addr = request.remote_addr
        logs.log(user + ' - ' + remote_addr + '- TerminosClinicos.get()')
        
        args = request.headers
        if args.get('user') is not None and args.get('token') is not None:
            user = args['user']
            token = args['token']
            login = crypto.verify_auth_token(token)
            if login is None or login != user:
                result = {'result': 'error', 'message': 'Invalid token'}
                #return jsonify(result)

            id = ''
            termino = ''
            if 'id' in args:
                id = args['id']
            if 'termino' in args:
                termino = args['termino']
            
            items = terminosclinicosmanager.select_terminosclinicos(user,remote_addr,id,termino)
            result = {'result':'success', 'data':items}
            return jsonify(result)

        else:
            result = {'result': 'error', 'message': 'Parametros incorrectos'}
            return jsonify(result)

class Users(Resource):

    #GET Users : Validacion de usuario
    def get(self):
        user = request.headers.get('user')
        remote_addr = request.remote_addr
        logs.log(user + ' - ' + remote_addr + '- Users.get()')
        
        #args = request.headers Recoger datos de la cabecer (header)
        #args = request.args Recoger parametros de la URL
        #args = flask_restful.reqparse.RequestParser().parse_args() Recoger argumentos de la llamada

        args = request.headers
        if args.get('user') is not None and args.get('password') is not None:
            user = args['user']
            password = args['password']
        else:
            result = {'result': 'error', 'message': 'Incorrect parameters'}
            return jsonify(result)
        try:
            validated = usersmanager.validateUser(user,password,remote_addr)
        except:
            result = {'result': 'error', 'message': 'Unknown error'}
            return jsonify(result)

        if validated is True:
            token = crypto.generate_auth_token(args['user'])
            result = {'result':'success', 'token':str(token.decode("utf-8"))}
            return jsonify(result)        
        else:
            result = {'result':'error', 'message': 'Incorrect user/password'}
            return jsonify(result)

class Reports(Resource):        
    #PUT Reports : Creación de Informes
    def put(self):
        user = request.headers.get('user')
        remote_addr = request.remote_addr
        logs.log(user + ' - ' + remote_addr + '- Studies.get()')
        args = request.headers
        if args.get('user') is not None and args.get('reportid') is not None and args.get('token') is not None:
            user = args['user']
            reportid = args['reportid']
            token = args['token']
            reportbody = request.data.decode()
            
            login = crypto.verify_auth_token(token)
            if login is None or login != user:
                result = {'result': 'error', 'message': 'Invalid token'}
                #return jsonify(result)
                
            if 'model' in args:
                inference_model = int(args['model'])
            else:
                inference_model = 0
           
        else:
            result = {'result': 'error', 'message': 'Parametros incorrectos'}
            return jsonify(result)
        
        try:

            report_id = reportsmanager.create_report(user, remote_addr, reportid, reportbody, inference_model)
            termino_reports = reportsmanager.get_termino_reports(user, remote_addr, report_id)

        except Exception as inst:
            result = {'result': 'error', 'message': 'Unknown error'}
            return jsonify(result)
        else:
            result = {'data': termino_reports, 'result':'success'}
            return jsonify(result)

    #GET Reports : Consulta de Informes
    def get(self):
        user = request.headers.get('user')
        remote_addr = request.remote_addr
        logs.log(user + ' - ' + remote_addr + '- Reports.get()')
        args = request.headers
        if args.get('user') is not None and args.get('token') is not None:
            user = args['user']
            token = args['token']
            login = crypto.verify_auth_token(token)
            if login is None or login != user:
                result = {'result': 'error', 'message': 'Invalid token'}
                #return jsonify(result)

            idreport=''
            owner=''
            termino=''
            if 'idreport' in args:
                idreport = args['idreport']
            if 'owner' in args:
                owner = args['owner']
            if 'termino' in args:
                termino = args['termino']
				
                
            
        else:
            result = {'result': 'error', 'message': 'Parametros incorrectos'}
            return jsonify(result)
        
        try:
            #if idtermino != '':
                #lista_reports = reportsmanager.get_reports(user, remote_addr, idtermino)
            #elif idreport != '':
                #lista_reports = reportsmanager.get_termino_reports(user, remote_addr, report_id, owner)
            #else:
            #lista_reports = reportsmanager.select_reports(user, remote_addr)
            lista_reports = reportsmanager.get_reports_and_labels(user, remote_addr, idreport, owner, termino)
        except Exception as inst:
            result = {'result': 'error', 'message': 'Unknown error'}
            return jsonify(result)
        else:
            result = {'data': lista_reports, 'result':'success'}
            return jsonify(result)

        

api.add_resource(Users, '/users') # Route_1
api.add_resource(Application, '/application') # Route_2
api.add_resource(TerminosClinicos, '/terminosclinicos') # Route_3
api.add_resource(Reports, '/reports') # Route_4
#api.add_resource(Tracks, '/tracks') # Route_2
#api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3

if __name__ == '__main__':

    if configuration.REST_SERVER_SSL:
        #SSL - Unstable !!!
        #Load SSL Cert
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(configuration.SSL_CERTIFICATE_CERT,configuration.SSL_CERTIFICATE_KEY,password=configuration.SSL_CERTIFICATE_PASSWORD)
        app.run(host=configuration.REST_SERVER_HOST,port=configuration.REST_SERVER_PORT,threaded=True,use_reloader=True, ssl_context=context)
    else:
        #HTTP
        #app.run(host=configuration.REST_SERVER_HOST,port=configuration.REST_SERVER_PORT,threaded=True,use_reloader=True)
        app.run(host=configuration.REST_SERVER_HOST,port=configuration.REST_SERVER_PORT,threaded=True,use_reloader=True,debug=True)
