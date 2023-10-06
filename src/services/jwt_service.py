import jwt
import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

"""
mkdir keys
openssl genpkey -algorithm RSA -out ./keys/chave_privada.pem
openssl rsa -pubout -in ./keys/chave_privada.pem -out ./keys/chave_publica.pem
"""
class JwtService():
    def __init__(self):
        pass

    def generate(self, payload):
        algoritmo = 'RS256'
        return jwt.encode(payload, self._get_private_key(), algorithm=algoritmo)
    
    def decode(self, token):
        try:
            payload = jwt.decode(token, self._get_public_key(), algorithms=['RS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def _get_private_key(self):
        with open('keys/chave_privada.pem', 'rb') as chave_privada_arquivo:
            chave_privada = chave_privada_arquivo.read()
            return chave_privada

    def _get_public_key(self):
        with open('keys/chave_publica.pem', 'rb') as chave_publica_arquivo:
            chave_publica = chave_publica_arquivo.read()
            return chave_publica

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={'items': 'permissions to access items'}
)