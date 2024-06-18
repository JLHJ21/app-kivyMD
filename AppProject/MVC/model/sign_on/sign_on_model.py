import database.database as DataBase
#from passlib.hash import sha256_crypt

name_collection = 'users'
API = DataBase.DatabaseClass

class SignOnDatabase():
    def CreateAccountDB(username, email, password):
                
        #collection = DataBase.db['users']

        #data

        if API.CountDocument(
            name_collection,
            {
                'username': username,
            },
            None,
            None
        ):
            return ', ya existe este nombre de usuario'

        #if collection.count_documents({'username': username}, limit = 1):
        #    return ', ya existe este nombre de usuario'

        elif API.CountDocument(
            name_collection,
            {
                'email': email,
            },
            None,
            None
        ):
            return ', ya existe este correo electrónico'
        
        else:

            '''
            0 = empleado
            1 = administrador
            2 = programador
            
            '''

            document = {'username': username, 'email': email, 'password': password, 'access_level': 0}

            API.InsertInto(
                name_collection, 
                document
            )


            #collection.insert_one(post)

            return True