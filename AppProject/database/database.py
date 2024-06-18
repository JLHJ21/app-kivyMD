#UNION/ENLACE CON LA BASE DE DATOS MONGODB

# import the MongoClient class
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from passlib.hash import sha256_crypt
from bson import ObjectId



import requests
import json

import certifi
#username: giwileb320
#password: w1ILQeJTCTtqVfba

#mongodb+srv://giwileb320:w1ILQeJTCTtqVfba@cluster0.m0ki2xc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0


#api key
#0GPikKUv5FT2DDEpA3jE7ulhZGlfqT1PmnEQNvtkihGxy4YaXdse8oViFae2d7UO
db = None

class DatabaseClass():

    headers = {
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': '*',
            'api-key': '0GPikKUv5FT2DDEpA3jE7ulhZGlfqT1PmnEQNvtkihGxy4YaXdse8oViFae2d7UO', 
            'return_type': 'JSON'
        }

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
        collection = db['products']

        collection.delete_many({})

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

    def Find(collection, filter_query, projection, skip, limit, sort):

        '''
        collection, se refiere a la coleccion(tabla en sql) que se utilizará en este query
        filter_query, se refiere al filtro que tendrá el query, ejm: cantidad': {"$ne" : "0"}, mostrará todos los documentos que la cantidad sea mayor a 0
        projection, se refiere a los "items" o atributos que se mostrarán solamente, ejm: {'_id': 1} solo mostrará el id más no los otros datos
        skip, salta la cantidad de documentos en el query
        limit, limita la cantidad de documentos que regresará el query
        sort, ordena los documentos entregados por el query, ya sea de mayor a menor o de menor a mayor
        '''
                
        #cambiar por la opcion, ahorita es find
        url = "https://us-east-1.aws.data.mongodb-api.com/app/data-rxxunxx/endpoint/data/v1/action/find"

        json_query = {
            "dataSource": "DataBaseIV",
            "database": "programDB",
        }

        if collection != None:
            json_query['collection'] = collection

        if filter_query != None:
            json_query['filter'] = filter_query

        
        if projection != None:
            json_query['projection'] = projection


        if skip != None:
            json_query['skip'] = skip

        if limit != None:
            json_query['limit'] = limit

        #"dataSource": "DataBaseIV",
        #"database": "programDB",

        #"collection": collection,
        #"projection": projection,
        #"filter": filter,
        #"skip": skip,
        #"limit": limit,
        #"sort": sort
            
        if sort != None:
            json_query['sort'] = sort

        #El query a buscar
        payload = json.dumps(
            json_query
        )

        response = requests.request("POST", url, headers=DatabaseClass.headers, data=payload)

        #transforma el json en dicitonario
        out = response.json()
        #print(response.text)
        #print(type(out))
        #print(out)

        #lo entrega tal y como lo permite el sistema    
        try:
            return out['documents']
        except:
            return None
            
    #no usar
    def FindOne(collection, filter_query, projection):
        
        '''
        collection, se refiere a la coleccion(tabla en sql) que se utilizará en este query
        filter, se refiere al filtro que tendrá el query, ejm: cantidad': {"$ne" : "0"}, mostrará todos los documentos que la cantidad sea mayor a 0
        projection, se refiere a los "items" o atributos que se mostrarán solamente, ejm: {'_id': 1} solo mostrará el id más no los otros datos
        '''
                
        #cambiar por la opcion, ahorita es find
        url = "https://us-east-1.aws.data.mongodb-api.com/app/data-rxxunxx/endpoint/data/v1/action/findOne"

        json_query = {
            "dataSource": "DataBaseIV",
            "database": "programDB",
        }

        if collection != None:
            json_query['collection'] = collection

        if projection != None:
            json_query['projection'] = projection

        if filter_query != None:
            json_query['filter'] = filter_query
        
        payload = json.dumps(
            json_query
        )

        response = requests.request("POST", url, headers=DatabaseClass.headers, data=payload)

        #transforma el json en dicitonario
        out = response.json()

        #lo entrega tal y como lo permite el sistema
        #return out['document']
    
        try:
            return out['document']
        except:
            return None
    
    def CountDocument(collection, match, skip, limit):
        '''
        collection, se refiere a la coleccion(tabla en sql) que se utilizará en este query
        match, se refiere a los productos a buscar (el project)
        skip, salta la cantidad de documentos en el query
        limit, limita la cantidad de documentos que regresará el query
        '''

        #primero tiene que ir el limit para que si limite los documentos a buscar
        #{"$limit": 1},
        #{"$skip": 0},
        #{'$match': {'state_product': 1, 'amount_product': {"$ne" : "0"} } },
        #{ '$group': { '_id': 1, 'amount_item': { '$sum': 1 } } },
                
        #cambiar por la opcion, ahorita es aggregate
        url = "https://us-east-1.aws.data.mongodb-api.com/app/data-rxxunxx/endpoint/data/v1/action/aggregate"

        pipeline_query = []

        if skip != None:
            add = {"$skip": skip}
            pipeline_query.append(add)

        if limit != None:
            add = {"$limit": limit}
            pipeline_query.append(add)

        add_match = {"$match": match}
        pipeline_query.append(add_match)

        add_match = { '$group': { '_id': 1, 'amount_item': { '$sum': 1 } } }
        pipeline_query.append(add_match)



        #"dataSource": "DataBaseIV",
        #"database": "programDB",

        #"collection": collection,
        #"projection": projection,
        #"filter": filter,
        #"sort": sort
        
        payload = json.dumps(
            {
            
                "dataSource": "DataBaseIV",
                "database": "programDB",
                "collection": collection,
                "pipeline": pipeline_query 
            }
        )


        response = requests.request("POST", url, headers=DatabaseClass.headers, data=payload)

        #transforma el json en dicitonario
        out = response.json()

        #lo entrega tal y como lo permite el sistema
        
        try:
            return out['documents'][0]['amount_item']
        except:
            return None
        
    def Aggregate(collection, match, skip, limit, project):
        '''
        collection, se refiere a la coleccion(tabla en sql) que se utilizará en este query
        match, se refiere a los productos a buscar (el project)
        skip, salta la cantidad de documentos en el query
        limit, limita la cantidad de documentos que regresará el query
        '''

        #primero tiene que ir el limit para que si limite los documentos a buscar
        #{"$limit": 1},
        #{"$skip": 0},
        #{'$match': {'state_product': 1, 'amount_product': {"$ne" : "0"} } },
        #{ '$group': { '_id': 1, 'amount_item': { '$sum': 1 } } },
                
        #cambiar por la opcion, ahorita es aggregate
        url = "https://us-east-1.aws.data.mongodb-api.com/app/data-rxxunxx/endpoint/data/v1/action/aggregate"

        pipeline_query = []

        if skip != None:
            add = {"$skip": skip}
            pipeline_query.append(add)

        if limit != None:
            add = {"$limit": limit}
            pipeline_query.append(add)

            
        add_match = {"$match": match}
        pipeline_query.append(add_match)
        
        add_match = { '$project': project }
        pipeline_query.append(add_match)

        payload = json.dumps(
            {
            
                "dataSource": "DataBaseIV",
                "database": "programDB",
                "collection": collection,
                "pipeline": pipeline_query
            }
        )


        response = requests.request("POST", url, headers=DatabaseClass.headers, data=payload)

        #transforma el json en dicitonario
        out = response.json()

        #lo entrega tal y como lo permite el sistema

        return out['documents']

    def UpdateOne(collection, filter, update):
        
        #cambiar por la opcion, ahorita es find
        url = "https://us-east-1.aws.data.mongodb-api.com/app/data-rxxunxx/endpoint/data/v1/action/updateOne"

        payload = json.dumps({
            "database": "programDB",
            "dataSource": "DataBaseIV",
            "collection": collection,

            "filter": filter,
            #"_id": { "$oid": "666e3f2e264f9279bfa8fa53" } 
            "update": {
            "$set": update
                #"state_product": 0
            }
        })

        response = requests.request("POST", url, headers=DatabaseClass.headers, data=payload)

        #transforma el json en dicitonario
        out = response.json()
        #lo entrega tal y como lo permite el sistema

        #print( out['modifiedCount'] )
        try:
            return out['modifiedCount'] >= 1
        except:
            return None
        
    
    def InsertInto(collection, document):

        '''
        collection, se refiere a la coleccion(tabla en sql) que se utilizará en este query
        filter_query, se refiere al filtro que tendrá el query, ejm: cantidad': {"$ne" : "0"}, mostrará todos los documentos que la cantidad sea mayor a 0
        projection, se refiere a los "items" o atributos que se mostrarán solamente, ejm: {'_id': 1} solo mostrará el id más no los otros datos
        skip, salta la cantidad de documentos en el query
        limit, limita la cantidad de documentos que regresará el query
        sort, ordena los documentos entregados por el query, ya sea de mayor a menor o de menor a mayor
        '''
                
        #cambiar por la opcion, ahorita es find
        url = "https://us-east-1.aws.data.mongodb-api.com/app/data-rxxunxx/endpoint/data/v1/action/insertOne"

        json_query = {
            "dataSource": "DataBaseIV",
            "database": "programDB",
            "collection": collection,

        }

        if document != None:

            json_query["document"] = document
        else:
            print('Error, falta el document/match en la función insertInto')
            return

        #El query a buscar
        payload = json.dumps(
            json_query
        )

        response = requests.request("POST", url, headers=DatabaseClass.headers, data=payload)

        #transforma el json en dicitonario
        out = response.json()
        #print(response.text)
        #print(type(out))
        #print(out)

        #lo entrega tal y como lo permite el sistema
        #print(out)
        #print()
        #print(json_query)

    




