#UNION/ENLACE CON LA BASE DE DATOS MONGODB

# import the MongoClient class
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from passlib.hash import sha256_crypt


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
    
    def CreateAccountDB(username, email, password):
                
        collection = db['users']

        #data

        if collection.count_documents({'username': username}, limit = 1):

            return 'USERNAME: ' + str(collection.find({'username': username}))

        elif collection.count_documents({'email': email}, limit = 1):
            return 'EMAIL: ' + str(collection.find({'email': email}))
        
        else:

            post = {'username': username, 'email': email, 'password': password}
            collection.insert_one(post)

            return True

    def SignInBD(username, password):
        
        collection = db['users']

        user = collection.find_one({"username": username})

        if user and sha256_crypt.verify(password, user['password']):
            return True

        return False




