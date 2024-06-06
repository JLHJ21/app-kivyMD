#UNION/ENLACE CON LA BASE DE DATOS MONGODB

# import the MongoClient class
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from passlib.hash import sha256_crypt
from bson import ObjectId


import certifi
#username: giwileb320
#password: w1ILQeJTCTtqVfba

#mongodb+srv://giwileb320:w1ILQeJTCTtqVfba@cluster0.m0ki2xc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

db = None

class DatabaseClass():

    def Conexion():


        # global variables for MongoDB host (default port is 27017)
        uri = "mongodb+srv://jorge:jorge123@databaseiv.yogxdsl.mongodb.net/?retryWrites=true&w=majority&appName=DataBaseIV"

        #uri = "mongodb://jorge:jorge123@ac-mstim7j-shard-00-00.yogxdsl.mongodb.net:27017,ac-mstim7j-shard-00-01.yogxdsl.mongodb.net:27017,ac-mstim7j-shard-00-02.yogxdsl.mongodb.net:27017/?replicaSet=atlas-p18cpb-shard-0&ssl=true&authSource=admin"
        # Create a new client and connect to the server
        #client = MongoClient(uri, server_api=ServerApi('1'))
        client = MongoClient(uri, server_api=ServerApi('1'),  tlsCAFile=certifi.where())

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")


            #GLOBAL VARIABLE DATABASE
                
            global db

            db = client['programDB']


        except Exception as e:
            print()
            print('ERROR AQUI ESTá!')
            print(e)

    def InsertData():
        '''
        collection = db['supplier']

        collection.delete_many({})

        for i in range(1,11):
            post= {
                'name_supplier': 'proveedor n°' + str(i),
                'address_supplier': 'Direccion Calle-' + str(i),
                'rif_supplier': 'R-30134727' + str(i),
                'phone_supplier': '0416-000000' + str(i),
                'state_supplier': 1
                }

            collection.insert_one(post)


        
        post= {
            'name_client': 'cliente n° 12',
            'id_client': 'V- 12',
            'phone_client': '0416-000000 12',
            'state_client': 1
            }

        collection.insert_one(post)

        '''
        
        collection_2 = db['charges']
        collection_2.delete_many({})

        for i in range(0,4):

            post = {
                "name_supplier": "proveedor n°4",
                "id_supplier": ObjectId("665bd24669ed9acabb259fea"),
                "products": [
                    {
                    "name_product": "Cantinflas" + str(i),
                    "amount_product": "1",
                    "buy_product": "4",
                    "profit_product": "6",
                    "id_product": ObjectId("66592ff5b4e6772e729fc25e"),

                    },
                    {
                    "name_product": "Harina" + str(i),
                    "amount_product": "2",
                    "buy_product": "3",
                    "profit_product": "5",
                    "id_product": ObjectId("6659294d982045ee417292fa"),
                    }
                ],
                "date": "30-05-2024 22:03:33",
                "buy_products": "10.000$",
                "profit_products": "16.000$",
                "total_money": "6.000$",
                "state": { "$numberInt": "1" }
            }

            collection_2.insert_one(post)
        
        '''
        collection = db['products']
        #collection.delete_many({})

        #data
        for i in range(0,5):

            post = {
                "name_supplier": "Cucuta Inversiones",
                "id_supplier": {
                    "_id": "66451d76b8dab420c06566f6"
                },
                "products": [
                    {
                    "name_product": "Cantinflas" + str(i),
                    "amount_product": "1",
                    "buy_product": "4",
                    "profit_product": "6",
                    "id_product": {
                        "_id": "6659294d982045ee417292fa"
                    }
                    },
                    {
                    "name_product": "Harina" + str(i),
                    "amount_product": "2",
                    "buy_product": "3",
                    "profit_product": "5",
                    "id_product": {
                        "_id": "66592ff5b4e6772e729fc25e"
                    }
                    }
                ],
                "date": "30-05-2024 22:03:33",
                "buy_products": "10.000$",
                "profit_products": "16.000$",
                "total_money": "6.000$",
                "state": { "$numberInt": "1" }
            }

            collection_2.insert_one(post)

        #collection.delete_many({})
        '''

    def GetDataSupplier(text):

        import re

        rgx = re.compile('.*'+ text +'.*', re.IGNORECASE)  # compile the regex


        collection = db['supplier']

        results = collection.find({'name': rgx}, {'name': 1}).limit( 5 )#.sort({ '_id' : ObjectId(last_id)})

        #SE CREA DICCIONARIO QUE ALMACENARÁ LOS DATOS OBTENIDOS DE LA BASE DE DATOS
        list_results = {}

        #CICLO FOR QUE AGREGA LOS DATOS OBTENIDO DE LA BASE DE DATOS AL DICCIONARIO LIST_RESULTS, ESTO HACE QUE LA VARIABLE RESULTS(CURSOR) SE VACIE 
        for index, i in enumerate(results):

            #LO ALMACENA DE FORMA, DATO(POSICION): 'TODA LA INFORMACIÓN DE LA BASE DE DATOS
            d = {f"dato{index}": i}

            list_results.update(d)

        

        #RETORNA LA INFORMACIÓN OBTENIDO
        return list_results


    




