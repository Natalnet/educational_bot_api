import datetime
from uuid import uuid4
from src.models.usuario import Usuario
from src.data.mongodb import connection
from src.exceptions import UserNotFoundException

roles = ['DISCENTE','DOCENTE','MONITOR','ADMIN']

class AdminService(): 
    
    def __init__(self):
        client = connection
        db = client.apibotdb
        self.collection = db.usuarios

    def registrar(self, usuario: Usuario):
        self.collection.insert_one({
            '_id': str(uuid4()),
            'discord_id': usuario.discord_id,
            'roles': [],
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        })
    
    def buscar(self, usuario_id: str):
        filter = {'_id': usuario_id }
        return self.collection.find_one(filter)

    def grant_role(self, discord_id: str, role: str):
        filter = {'discord_id': discord_id }
        user = self.collection.find_one(filter)

        if user is None:
            return UserNotFoundException

        user_roles = user['roles']
        if role not in user_roles:
            user_roles.append(role)

        user_updated = { '$set': {
            'roles': user_roles,
            'updated_at': datetime.datetime.now()
        }}

        self.collection.update_one(filter, user_updated)

    def revoke_role(self, discord_id: str, role: str):
        filter = {'discord_id': discord_id }
        user = self.collection.find_one(filter)

        if user is None:
            return UserNotFoundException
        
        user_roles = user['roles']
        if role in user_roles:
            user_roles.remove(role)

        user_updated = { '$set': {
            'roles': user_roles,
            'updated_at': datetime.datetime.now()
        }}

        self.collection.update_one(filter, user_updated)