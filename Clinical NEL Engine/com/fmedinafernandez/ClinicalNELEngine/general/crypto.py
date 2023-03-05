'''
Created on 27 dec. 2022

@author: fmedinafernandez
'''
#pip install itsdangerous==2.0.1
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
import com.fmedinafernandez.ClinicalNELEngine.general.configuration as configuration
import com.fmedinafernandez.ClinicalNELEngine.general.logs as logs

SECRET_KEY = configuration.CRYPTO_SECRET_KEY
CRYPTO_TOKEN_EXPIRATION = configuration.CRYPTO_TOKEN_EXPIRATION


def generate_auth_token(id, expiration = CRYPTO_TOKEN_EXPIRATION):
    logs.log("crypto.generate_auth_token('"+id+"',"+str(expiration)+")")
    s = TimedJSONWebSignatureSerializer(
           SECRET_KEY,
           expires_in = expiration
           )
    return s.dumps({ 'id': id })
    
def verify_auth_token(token):
    logs.log("crypto.verify_auth_token('"+token+"')")
    s = TimedJSONWebSignatureSerializer(SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    return data['id']