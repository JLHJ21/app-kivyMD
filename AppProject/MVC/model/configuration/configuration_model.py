import database.database as DataBase

from passlib.hash import sha256_crypt
import MVC.controller.functions as functions


name_collection = 'users'
API = DataBase.DatabaseClass

class ConfigurationBD():
    def ChangeUserData(indexData, value1, value2):
        
        
        #collection = DataBase.db['users']

        #busca si existe un usuario con el dato dado
        #user = collection.find_one({"username": functions.usernameStaff})


        #if user:
        #if value1 == value2:

        match indexData:
            case 'password':
                    value1 = sha256_crypt.hash(value1)

            #    if sha256_crypt.verify(value1, functions.passwordStaff):
            #        return ', la contraseña es identica a la existente.'
            #    else:
            #        value1 = sha256_crypt.hash(value1)
            case 'email':

                
                if API.CountDocument(
                        name_collection,
                        {'email': value1},
                        None,
                        None
                    ):
                    return ', ya existe este correo electrónico.'

                #if collection.count_documents({'email': value1}, limit = 1):
                #    return ', ya existe este correo electrónico.'
                
                #elif value1 == functions.usernameStaff:
                #    return ', el correo es el mismo.'

            case 'username':
                if API.CountDocument(
                        name_collection,
                        {'username': value1},
                        None,
                        None
                    ):
                    return ', ya existe este usuario.'

                #if collection.count_documents({'username': value1}, limit = 1):
                #    return ', ya existe este usuario.'
                
                #elif value1 == functions.usernameStaff:
                #    return ', el usuario es el mismo.'

        newValue = { indexData: value1 }

        API.UpdateOne(
                    name_collection,
                    {'_id': {'$oid':  functions.idStaff}},
                    newValue
                )
        #documentToChange = { 'username': functions.usernameStaff}
        #newValue = { "$set": { indexData: value1 } }

        #collection.update_one(documentToChange, newValue)
        
        match indexData:
            case 'username':
                functions.usernameStaff = value1
                
            case 'email':
                functions.emailStaff = value1

            case 'password':
                functions.passwordStaff = value1

        return True
                
        #else:
        #    return ', los datos no son iguales.'
        
        #else:
        #    print('no se encuentra el usuario')


        #pass