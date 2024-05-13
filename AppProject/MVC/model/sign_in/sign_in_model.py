import database.database as DataBase
import MVC.controller.home.home_controller as Home
import MVC.controller.configuration.configuration_controller as Configuration

import MVC.controller.functions as functions

from passlib.hash import sha256_crypt

class SignInDatabase():
    def SignInBD(username, password):
        
        
        collection = DataBase.db['users']

        #busca si existe un usuario con el dato dado
        user = collection.find_one({"username": username})

        #verifica si la contraseña es igual al dato dato
        if user and sha256_crypt.verify(password, user['password']):

            #cambia los datos que se muestran en HomePage

            functions.username_text = user['username']
            functions.email_text = user['email']
            functions.password_text = user['password']
            functions.access_text = user['access_level']

            #Configuration.ConfigurationPage.username_text = 


            return True

        return False