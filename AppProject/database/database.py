#UNION/ENLACE CON LA BASE DE DATOS MONGODB

# import the MongoClient class
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi


db = None

class DatabaseClass():

    def Conexion():


        # global variables for MongoDB host (default port is 27017)
        uri = "mongodb+srv://jorge:jorge123@databaseiv.yogxdsl.mongodb.net/?retryWrites=true&w=majority&appName=DataBaseIV"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")


            #GLOBAL VARIABLE DATABASE
                
            global db

            db = client['programDB']


        except Exception as e:
            print(e)

    def InsertData():
        collection = db['foreign_exchange']

        #data
        post = {'name': 'Dólar', 'changeToDolar': '1', 'changeToPeso': '4000', 'changeToBolivar': '36,56', 'preference': False}
        post2 = {'name': 'Peso', 'changeToDolar': '4000', 'changeToPeso': '1000', 'changeToBolivar': '9,39', 'preference': False}
        post3 = {'name': 'Bolívar', 'changeToDolar': '36,56', 'changeToPeso': '106,51', 'changeToBolivar': '1', 'preference': False}


        collection.insert_many([post, post2, post3])

    def ChangePreferenceExchangeForeign(preference = None):

        collection = db['foreign_exchange']
        dataList = []

        if preference == None:
            pass
        else:
            #FALSO LA PREFERENCIA
            documentToChange = { 'preference': True}
            newValue = { "$set": { "preference": False } }

            collection.update_one(documentToChange, newValue)


            #TRUE LA PREFERENCIA
            documentToChange = { "name": preference }
            newValue = { "$set": { "preference": True } }

            collection.update_one(documentToChange, newValue)

        results = collection.find_one({'preference': True})

        #Valores
        dolar = results['changeToDolar']
        peso = results['changeToPeso']
        bolivar = results['changeToBolivar']
        nombre = results['name']


        dataList.extend([dolar, peso, bolivar, nombre])

        return dataList

    def UpdateForeignExchangeData(dolar, peso, bolivar):


        #DOLAR
        if len(dolar) < 1:

            #DOLAR
            documentToChange = { "name": 'dolar' }
            newValue = { "$set": { "changeToPeso": peso, "changeToBolivar": bolivar } }

        #PESO
        elif len(peso) < 1:
            #PESO
            documentToChange = { "name": 'peso' }
            newValue = { "$set": { "changeToDolar": dolar, "changeToBolivar": bolivar } }

        #BOLIVAR
        elif len(bolivar) < 1:
            #BOLIVAR
            documentToChange = { "name": 'bolivar' }
            newValue = { "$set": { "changeToDolar": dolar, "changeToPeso": peso } }


        collection = db['foreign_exchange']
        collection.update_one(documentToChange, newValue)
      

    def ShowDataExchangeForeign(name):
        collection = db['foreign_exchange']
        dataList = []
        

        results = collection.find_one({'preference': True})

        dataList.append(results['changeToDolar'])

        return dataList

        #print(results['changeToDolar'])


