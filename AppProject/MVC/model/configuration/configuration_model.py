import database.database as DataBase

from passlib.hash import sha256_crypt
import MVC.controller.functions as functions

class ConfigurationBD():
    def ChangeUserData(indexData, value1, value2):
        
        
        collection = DataBase.db['users']

        #busca si existe un usuario con el dato dado
        user = collection.find_one({"username": functions.username_text})


        if user:

            if value1 == value2:


                if indexData == 'password':
                    if sha256_crypt.verify(value1, user[indexData]):
                        print(' son iguales los datos password en la bd no se cambiaran')
                        return
                    else:
                        value1 = sha256_crypt.hash(value1)

                elif value1 == user[indexData]:
                    print(' son iguales los datos en la bd no se cambiaran')
                    return

        
                documentToChange = { 'username': functions.username_text}
                newValue = { "$set": { indexData: value1 } }



                collection.update_one(documentToChange, newValue)
                
                match indexData:
                    case 'username':
                        functions.username_text = value1
                        
                    case 'email':
                        functions.email_text = value1

                    case 'password':
                        functions.password_text = value1

                return
                    
            else:
                print('no son iguales')
        
        else:
            print('no se encuentra el usuario')


        pass