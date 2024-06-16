import database.database as DataBase
from passlib.hash import sha256_crypt

class SignOnDatabase():
    def CreateAccountDB(username, email, password):
                
        collection = DataBase.db['users']

        #data

        if collection.count_documents({'username': username}, limit = 1):
            return ', ya existe este nombre de usuario'

        elif collection.count_documents({'email': email}, limit = 1):
            return ', ya existe este correo electrónico'
        
        else:

            '''
            0 = empleado
            1 = administrador
            2 = programador
            
            '''

            post = {'username': username, 'email': email, 'password': password, 'access_level': 0}
            collection.insert_one(post)

        return True