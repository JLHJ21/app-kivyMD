import database.database as DataBase
#from passlib.hash import sha256_crypt
import MVC.controller.functions as functions

name_collection = "users"
#API = DataBase.DatabaseClass

class SignOnDatabase():
    def CreateAccountDB(username, email, password):
                

        query_count_username = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "username": username
                },
        }

        query_count_email = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "email": email,
                },
        }

        #data
        if functions.FunctionsKivys.GetResultFromDatabase(query_count_username, 'count_document'):
            return ', ya existe este nombre de usuario'
        
        elif functions.FunctionsKivys.GetResultFromDatabase(query_count_email, 'count_document'):
            return ', ya existe este correo electrónico'
        
        else:

            '''
            0 = empleado
            1 = administrador
            2 = programador
            
            '''

            query_insert = {
                #nombre de la colección
                "collection_choose": name_collection, 
                #datos a agregar en la coleccion
                "document_insert":
                    {
                        "username": username, 
                        "email": email, 
                        "password": password, 
                        "access_level": 0
                    },
                
                }

            result = functions.FunctionsKivys.GetResultFromDatabase(query_insert, 'insert_into')

            return result