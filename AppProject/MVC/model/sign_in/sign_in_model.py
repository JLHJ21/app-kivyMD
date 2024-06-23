import database.database as DataBase
import MVC.controller.home.home_controller as Home
import MVC.controller.configuration.configuration_controller as Configuration

import MVC.controller.functions as functions

from passlib.hash import sha256_crypt
import json

name_collection = "users"
API = DataBase.DatabaseClass

class SignInDatabase():
    def SignInBD(username, password):
        
        
        #collection = DataBase.db['users']

        #busca si existe un usuario con el dato dado
        #user = collection.find_one({"username": username})

        query = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "username": username
                },
            #dato a mostrar
            "projection": "None",
            #cantidad de archivos a saltar
            "skip":0,
            #cantidad de resultados
            "limit": 0,
            #como se ordenarán
            "sort": {
                "_id":-1
            }
        }
        
        user = functions.FunctionsKivys.GetResultFromDatabase(query, "find_one")

        #user = API.FindOne(
        #    name_collection,
        #    {"username": username},
        #    None
        #)

        #verifica si la contraseña es igual al dato dato
        if user and sha256_crypt.verify(password, user['password']):

            #cambia los datos que se muestran en HomePage

            functions.idStaff = user['_id']
            
            functions.usernameStaff = user['username']
            functions.emailStaff = user['email']
            functions.passwordStaff = user['password']

            functions.access_text = user['access_level']

            #Configuration.ConfigurationPage.username_text = 


            return True

        return False