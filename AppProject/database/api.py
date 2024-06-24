from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
import json
import json
from bson import json_util, ObjectId

app = Flask(__name__)


#credenciales
mongo_uri = "mongodb+srv://jorge:jorge123@databaseiv.yogxdsl.mongodb.net/?retryWrites=true&w=majority&appName=DataBaseIV"
client = MongoClient(mongo_uri, server_api=ServerApi('1'),  tlsCAFile=certifi.where())
db = client['programDB']
collection_test = db['products']


def TransformToObjectId(value):
    
    if "objectid" in value.lower():

        value = value.replace("'", "")

        value = value.replace("(", "")
        value = value.replace(")", "")

        value = value.replace("ObjectId", "")

        value = ObjectId(value)

        return value
    
def TransformToString(value, key, dictionary, indexes = '', haveIndex = False):


    if haveIndex:
        if type(value) == ObjectId:
            dictionary[indexes][key] = str(value)

        elif type(value) == dict:

            for v, k in zip(value.values(), value.keys()):
                if type(v) == ObjectId:
                    dictionary[indexes][key][k] = str(v)

    else:
        if type(value) == ObjectId:
            dictionary[key] = str(value)

        elif type(value) == dict:

            for v, k in zip(value.values(), value.keys()):
                if type(v) == ObjectId:
                    dictionary[key][k] = str(v)

#definicion de rutas

@app.route('/find', methods=['POST'])
def find():
    #coleccion de la base de datos a buscar 
    collection_choose = request.json['collection_choose']
    filter_query = request.json['search_query']
    projection = request.json['projection']
    skip = request.json['skip']
    limit = request.json['limit']
    sort = request.json['sort']

    collection = db[collection_choose]

    #No se pueden enviar comillas simples por el url
    
    ###############
    '''
    Convierte el texto, para que lo puedan leer el mongoDB
    '''

    if filter_query == 'None':
        filter_query = {}
    else:
        for value, key in zip(filter_query.values(), filter_query.keys()):
            try:
                if "objectid" in value.lower():

                    filter_query[key] = TransformToObjectId(value)
            
            except Exception as e:

                if type(value) == dict:
                    for i, k in zip(value.values(), value.keys()):

                        

                        try:
                            if "objectid" in i.lower():
                                filter_query[key][k] = TransformToObjectId(i)
                        except Exception as e:
                            print('segundo except, 104 linea')
                            

    if projection == 'None':
        projection = {}

            
    #convierte las comillas dobles a comillas simples
    #projection = json.loads(projection)

    if sort == 'None':
        sort = {'_id': 1}

    ###############
    '''
    Convierte los numeros string a ints
    '''
    if skip == 'None':
        skip = 0
    else:
        #transforma el str a int, para que lo permita leer el mongodb
        skip = int(skip) 


    if limit == 'None':
        limit = 0
    else:
        #transforma el str a int, para que lo permita leer el mongodb
        limit = int(limit)


    #obtiene el resultado en Cursos.Object
    results = collection.find(filter_query, projection).skip(skip).limit(limit).sort(sort)


    #transforma el cursor a lista    
    try:
        result_list = list(results)
    except:
        return jsonify(list(results)), 200


    for index in range(0, len(result_list)):

            
        for value, key in zip(result_list[index].values(), result_list[index].keys()):

            TransformToString(value, key, result_list, index, True)


    #cambiar el ObjectId a String para que lo puede utilizar jsonify

    #envia los resultados con estatus 200 (Ok)
    return jsonify(result_list), 200

@app.route('/find_one', methods=['POST'])
def find_one():

    collection_choose = request.json['collection_choose']
    filter_query = request.json['search_query']
    projection = request.json['projection']

    #coleccion de la base de datos a buscar 
    collection = db[collection_choose]
    #No se pueden enviar comillas simples por el url

    
    ###############
    '''
    Convierte el texto, para que lo puedan leer el mongoDB
    '''

    if filter_query == 'None':
        filter_query = {}
    else:

        for value, key in zip(filter_query.values(), filter_query.keys()):
            try:
                if "objectid" in value.lower():

                    filter_query[key] = TransformToObjectId(value)
            
            except Exception as e:

                if type(value) == dict:
                    for i, k in zip(value.values(), value.keys()):

                        filter_query[key][k] = TransformToObjectId(i)

    if projection == 'None':
        projection = {}
    
    #obtiene el resultado en Cursos.Object
    result = collection.find_one(filter_query, projection)


    #cambiar el ObjectId a String para que lo puede utilizar jsonify
    try:
        for value, key in zip(result.values(), result.keys()):

            TransformToString(value, key, result)

    except Exception as e:
        return_result = []
        return jsonify(return_result), 200

    #envia los resultados con estatus 200 (Ok)
    return jsonify(result), 200

@app.route('/update_one', methods=['POST'])
def update_one():

    collection_choose = request.json['collection_choose']

    find_query = request.json['search_query']
    update_query = request.json['update_query']

    #coleccion de la base de datos a buscar 
    collection = db[collection_choose]

    '''
    Convierte el id en ObjectId, para que lo puedan leer el mongoDB
    '''
    
    for value, key in zip(find_query.values(), find_query.keys()):
        try:

            find_query[key] = TransformToObjectId(value)
        
        except Exception as e:

            if type(value) == dict:
                for i, k in zip(value.values(), value.keys()):

                    find_query[key][k] = TransformToObjectId(i)

    #No se pueden enviar comillas simples por el url    
    ###############
    '''
    Convierte el texto, para que lo puedan leer el mongoDB
    '''

    #try:
        #convierte las comillas dobles a comillas simples
    #    update_query = json.loads(update_query)
    #except:
    #    print('Error, el update_query no es un query')

    #obtiene el resultado en Cursos.Object
    results = collection.update_one(find_query, update_query)

    #results = collection.find_one(filter_query, projection)

    #cambiar el ObjectId a String para que lo puede utilizar jsonify
    #results['_id'] = str(results['_id'] )

        
    #envia los resultados con estatus 200 (Ok)
    #return jsonify(results), 200

    if results.modified_count >= 1:
        return jsonify(True), 200
 
    else:
        return jsonify(False), 500
    


@app.route('/insert_into', methods=['POST'])
def insert_into():

    collection_choose = request.json['collection_choose']
    document_insert = request.json['document_insert']

    #coleccion de la base de datos a buscar 
    collection = db[collection_choose]
    #No se pueden enviar comillas simples por el url
    ###############
    '''
    Convierte el texto, para que lo puedan leer el mongoDB
    '''

    for value, key in zip(document_insert.values(), document_insert.keys()):
        try:
            if "objectid" in value.lower():

                document_insert[key] = TransformToObjectId(value)


                '''
                value = value.replace("'", "")

                value = value.replace("(", "")
                value = value.replace(")", "")

                value = value.replace("ObjectId", "")

                value = ObjectId(value)

                document_insert[key] = value
                '''
        
        except Exception as e:

            if type(value) == dict:
                for i, k in zip(value.values(), value.keys()):
                    if "objectid" in i.lower():

                        document_insert[key][k] = TransformToObjectId(i)
                        '''
                        i = i.replace("'", "")

                        i = i.replace("(", "")
                        i = i.replace(")", "")

                        i = i.replace("ObjectId", "")

                        i = ObjectId(i)
                        document_insert[key][k] = i
                        '''


    #obtiene el resultado en Cursos.Object
    results = collection.insert_one(document_insert)

    #envia los resultados con estatus 200 (Ok)
    return jsonify(results.acknowledged), 200
    

@app.route('/count_document', methods=['POST'])
def count_document():

    collection_choose = request.json['collection_choose']
    count_query = request.json['search_query']
    skip = request.json['skip']
    limit = request.json['limit']
    
    haveSkip = True
    haveLimit = True

    #coleccion de la base de datos a buscar 
    collection = db[collection_choose]
    #No se pueden enviar comillas simples por el url

    if skip == 'None':
        haveSkip = False
    
    if limit == 'None':
        haveLimit = False

    '''
    Convierte el id en ObjectId, para que lo puedan leer el mongoDB
    '''

    for value, key in zip(count_query.values(), count_query.keys()):
        #if "objectid" in value.lower():

        #    count_query[key] = TransformToObjectId(value)

        try:
            if "objectid" in value.lower():
                count_query[key] = TransformToObjectId(value)
        
        except Exception as e:

            if type(value) == dict:
                for i, k in zip(value.values(), value.keys()):
                    try:
                        if "objectid" in i.lower():

                            count_query[key][k] = TransformToObjectId(i)
                    except:
                        if "objectid" in i[0].lower():

                            count_query[key][k][0] = TransformToObjectId(i[0])
                        print(count_query[key][k][0])
                        
    ###############


    #OJO
    if haveSkip and haveLimit:
        results = collection.count_documents(count_query, skip=skip, limit=limit)
    elif haveSkip:
        results = collection.count_documents(count_query, skip=skip)
    elif haveLimit:
        results = collection.count_documents(count_query, limit=limit)
    else:
        results = collection.count_documents(count_query)
        
    #envia los resultados con estatus 200 (Ok)
    return jsonify(results), 200



@app.route('/aggregate', methods=['POST'])
def aggregate():

    collection_choose = request.json['collection_choose']
    match_query = request.json['search_query']
    limit = request.json['limit']
    projection = request.json['projection']

    
    #coleccion de la base de datos a buscar 
    collection = db[collection_choose]
    #No se pueden enviar comillas simples por el url

    '''
    Convierte el id en ObjectId, para que lo puedan leer el mongoDB
    '''
    for value, key in zip(match_query.values(), match_query.keys()):
        if "objectid" in value.lower():

            match_query[key] = TransformToObjectId(value)
    #try:
    #    match_query['_id'] = ObjectId(match_query['_id'])
    #except:
    #    pass
    
    
    ###############
    
    aggregate_query = []

    add = {'$match': match_query}
    aggregate_query.append(add)

    add = {'$project': projection}

    aggregate_query.append(add)

    #si el limite es diferente a None, lo agrega al aggregate_query
    if limit != 'None':
        #si el numero dado es diferente o mayor a 0
        if limit > 0:
            add = {'$limit': limit}
            aggregate_query.append(add)
        else:
            #add = {'$limit': 0}
            print('el limite  es menor a 0, linea 525 API')

    #obtiene el resultado en Cursos.Object
    results = collection.aggregate(aggregate_query)
    
    #results_list = list(results)
    #envia los resultados con estatus 200 (Ok)
    return jsonify(list(results)), 200
    
if __name__ == '__main__':
    app.run(debug=True)
