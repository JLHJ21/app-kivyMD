import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId
import MVC.controller.functions as functions

last_id = previous_id = None

name_collection = 'clients'
#API = DataBase.DatabaseClass
class ClientsDB():



    def ShowData(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        #collection = DataBase.db['clients']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        #starting_id = collection.find({'state_client': 1})

        #starting_id = API.Find(
        #    name_collection,
        #    {'state_client': 1},
        #    {'_id': 1},
        #    None,
        #    None,
        #    {'id': -1}
        #)

        query = {
            "collection_choose": name_collection, 
            "search_query":
                {
                    'state_client': 1
                },
            "projection": {'_id': 1},
            "skip": 0,
            "limit": 0,
            "sort": "None"
        }

        starting_id = functions.FunctionsKivys.GetResultFromDatabase(query, 'find')

        #SI EL ESTADO ES NONE, REINICIA LAS VARIABLES GLOBALES
        if state == '':
            last_id = previous_id = None

        #SE ACTIVA AL SER LA PRIMERA LLAMADA A LA BASE DE DATOS
        if last_id == None:

            #OBTIENE LOS DATOS DE LA COLECCION

            #results = API.Find(
            #    name_collection, 
            #    {'state_client': 1},
            #    {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1},
            #    start, 
            #    end, 
            #    {'_id': 1}
            #)

            query_find = {
                "collection_choose": name_collection, 
                "search_query":
                    {'state_client': 1},
                "projection": {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1},
                "skip": start,
                "limit": end,
                "sort": "None"
            }
            
            #OBTIENE LOS DATOS DE LA COLECCION
            results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

            #results = collection.find({'state_client': 1}, {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1}).skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})
            
            #cantidad de productos que se encontraron
            #amount_items = API.CountDocument(
            #    name_collection,
            #    {'state_client': 1},
            #    start,
            #    end
            #)

            query_count = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {'state_client': 1},
                "skip": start,
                "limit": end
            }

            #cantidad de productos que se encontraron
            amount_items = functions.FunctionsKivys.GetResultFromDatabase(query_count, 'count_document')
            #amount_items = collection.count_documents({'state_client': 1}, skip=start, limit=end)

            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':

                query_find = {
                    "collection_choose": name_collection, 
                    "search_query":
                        {
                            "_id": 
                                {"$gt": 
                                    "ObjectId('" + last_id + "')"
                                }, 
                            'state_client': 1
                        },
                    "projection":
                        {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1},
                    "skip": "None",
                    "limit": end,
                    "sort": "None"
                }

                results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

                #results = API.Find(
                #    name_collection, 
                #    {'_id': {'$gt': { "$oid": last_id}}, 'state_client': 1},
                #    {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1},
                #    None, 
                #    end, 
                #    None
                #)

                #results = collection.find({'_id': {'$gt': last_id}, 'state_client': 1}, {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                #results1 = collection.find({'_id': {'$gt': last_id}}).limit( end )#.sort({ '_id' : ObjectId(last_id)})
                #amount_items = API.CountDocument(
                #    name_collection,
                #    {'_id': {'$gt': { "$oid": last_id}}, 'state_client': 1},
                #    None,
                #    end
                #)
                #amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_client': 1}, limit=end)

                query_count = {
                    #nombre de la coleccion
                    "collection_choose": name_collection, 
                    #archivo a buscar
                    "search_query":  
                        {
                            "_id": 
                                {"$gt": 
                                    "ObjectId('" + last_id + "')"
                                }, 
                            'state_client': 1
                        },
                    "skip": "None",
                    "limit": end
                }


                amount_items = functions.FunctionsKivys.GetResultFromDatabase(query_count, 'count_document')
                #last_item = len(list(results1)) - 1
                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':
                #results = collection.find({'_id': {'$gte': previous_id}, 'state_client': 1}, {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})
                
                #results = API.Find(
                #    name_collection, 
                #    {'_id': {'$gte': { "$oid": previous_id}}, 'state_client': 1},
                #    {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1},
                #    None, 
                #    end, 
                #    None
                #)

                query_find = {
                    "collection_choose": name_collection, 
                    "search_query":
                        {
                            "_id": 
                                {
                                    '$gte': "ObjectId('" + previous_id + "')"  
                                }, 
                                 
                            'state_client': 1, 
                        },
                    "projection":
                        {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1},
                    "skip": "None",
                    "limit": end,
                    "sort": "None"
                }

                results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

                #amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_client': 1}, limit=end)
                
                #amount_items = API.CountDocument(
                #    name_collection,
                #    {'_id': {'$gte': {"$oid": previous_id }}, 'state_client': 1},
                #    None,
                #    end
                #)

                query_count = {
                    #nombre de la coleccion
                    "collection_choose": name_collection, 
                    #archivo a buscar
                    "search_query": 
                        {'_id': 
                            {'$gte': "ObjectId('"+ previous_id +  "')"  }, 
                            'state_client': 1
                        },
                    "skip": "None",
                    "limit": end
                }

                amount_items = functions.FunctionsKivys.GetResultFromDatabase(query_count, 'count_document')
                

                #OBTIENE EL ULTIMO ID DEL ITEM DE LA COLECCION
                last_id = results[amount_items - 1]['_id']

                if (start - end) - 1 < 0:
            
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

        #SE CREA DICCIONARIO QUE ALMACENARÁ LOS DATOS OBTENIDOS DE LA BASE DE DATOS
        list_results = {}
        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        #numbers_collection = API.CountDocument(
        #            name_collection,
        #            {'state_client': 1},
        #            None,
        #            None
        #        )
        
        query_count = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {'state_client': 1},
            "skip": "None",
            "limit": "None"
        }

        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        numbers_collection = functions.FunctionsKivys.GetResultFromDatabase(query_count, 'count_document')
        #numbers_collection = collection.count_documents({'state_client': 1})#, skip=start, limit=end)

        #SE AGREGA SIEMPRE COMO PRIMER DATO, LAS CARACTERISTICAS (CANTIDAD DE DOCUMENTOS, ARCHIVO COMIENZA, ARCHIVO TERMINADA)
        list_results.update({'characteristics': [numbers_collection, start, end]})


        #CICLO FOR QUE AGREGA LOS DATOS OBTENIDO DE LA BASE DE DATOS AL DICCIONARIO LIST_RESULTS, ESTO HACE QUE LA VARIABLE RESULTS(CURSOR) SE VACIE 
        for index, i in enumerate(results):

            #LO ALMACENA DE FORMA, DATO(POSICION): 'TODA LA INFORMACIÓN DE LA BASE DE DATOS
            d = {f"dato{index}": [i]}

            list_results.update(d)

        #RETORNA LA INFORMACIÓN OBTENIDO
        return list_results


    def CreateClient(name, id, phone):
            
        #collection = DataBase.db['clients']

        query_count_document_name = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    'name_client': name,
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_name_client = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_name, 'count_document')
        print(result_name_client)
        #id
        query_count_document_id = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    'id_client': id,
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_id_client = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_id, 'count_document')
        print(result_id_client)

        #phone
        query_count_document_phone = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    'phone_client': phone,
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_phone = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_phone, 'count_document')
        print(result_phone)

        if result_name_client >= 1:
            print('nombre')
            return ', ya existe un nombre así.'
            #if API.CountDocument(
            #    name_collection,
            #    {
            #        'name_client': name,
            #    },
            #    None,
            #    None
            #):
            #    return 'ya existe un nombre así.'
            
            #if collection.count_documents({'name_client': name}, limit = 1):

            #    return 'ya existe un nombre así.'
        elif result_id_client >= 1:
            print('cedula')
            return ', ya existe una cédula así registrada.'   

            #elif API.CountDocument(
            #    name_collection,
            #    {
            #        'id_client': id,
            #    },
            #    None,
            #    None
            #):
            #    return 'ya existe una cédula así registrada.'   
            #elif collection.count_documents({'id_client': id}, limit = 1):
                #return 'ya existe una cédula así registrada.'

        elif result_phone >= 1:
            print('teléfono')
            return ', ya existe un teléfono así.'   

            #elif API.CountDocument(
            #    name_collection,
            #    {
            #        'phone_client': phone,
            #    },
            #    None,
            #    None
            #):
            #    return 'ya existe un teléfono así.'   
            #elif collection.count_documents({'phone_client': phone}, limit = 1):
            #    return 'ya existe un teléfono así.'
            
        else:

            print('else')
            #data
            #document = {'name_client': name, 'id_client': id, 'phone_client': phone, 'state_client': 1}
            #collection.insert_one(post)

            #API.InsertInto(
            #    name_collection, 
            #    document
            #)

            query_insert = {
                #nombre de la colección
                "collection_choose": name_collection, 
                #datos a agregar en la coleccion
                "document_insert":
                    {'name_client': name, 'id_client': id, 'phone_client': phone, 'state_client': 1}
            }

            result = functions.FunctionsKivys.GetResultFromDatabase(query_insert, 'insert_into')

            print()
            print()

            print(result)
            
            return result
    
    def UpdateClient(nameClient, idClient, phoneClient, idObject):
        
        query = {}
        #collection = DataBase.db['clients']
        query_count_document_name = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": {"$nin" : [ "ObjectId('" + idObject + "')" ]},
                    'name_client': nameClient,
                    "state_client": 1
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_name_client = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_name, 'count_document')

        #rif
        query_count_document_rif = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": {"$nin" : [ "ObjectId('" + idObject + "')" ]},
                    'name_client': nameClient,
                    "state_client": 1
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_rif = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_rif, 'count_document')

        #phone
        query_count_document_phone = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": {"$nin" : [ "ObjectId('" + idObject + "')" ]},
                    'phone_client': phoneClient,
                    "state_client": 1
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_phone = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_phone, 'count_document')

        if result_name_client >= 1:
            return ', ya existe registrado este nombre.'


        #Revisa si el dato existe en otros proveedores
        #if API.CountDocument(
        #        name_collection,
        #        {
        #            "_id": {"$nin" : [{ "$oid": idObject }]},
        #            'name_client': nameClient,
        #            "state_client": 1
        #        },
        #        None,
        #        None
        #    ):
        #    return ', ya existe registrado este nombre.'

        #if collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        'name_client': nameClient,
        #        "state_client": 1
        #    }):
            #return ', ya existe registrado este nombre.'
        elif result_rif >= 1:
            return ', ya existe registrado esta cédula.'

        #elif API.CountDocument(
        #        name_collection,
        #        {
        #            "_id": {"$nin" : [{ "$oid": idObject }]},
        #            'id_client': idClient,
        #            "state_client": 1
        #        },
        #        None,
        #        None
        #    ):
        #    return ', ya existe registrado esta cédula.'
        #elif collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        'id_client': idClient,
        #        "state_client": 1
        #    }):
        #    return ', ya existe registrado esta cédula.'

        elif result_phone >= 1:
            return ', ya existe registrado este número de teléfono.'

        #elif API.CountDocument(
        #        name_collection,
        #        {
        #            "_id": {"$nin" : [{ "$oid": idObject }]},
        #            'phone_client': phoneClient,
        #            "state_client": 1
        #        },
        #        None,
        #        None
        #    ):
        #    return ', ya existe registrado este número de teléfono.'

        #elif collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        'phone_client': phoneClient,
        #        "state_client": 1
        #    }):
        #    return ', ya existe registrado este número de teléfono.'
        else:

            #data

            ####Si no existe el dato introducido, lo añade al query
            #name_client

            query_count_document_name = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idObject + "')",
                        'name_client': nameClient,
                    },
                
                "skip": "None",
                "limit": "None"
            }
            result_name_product = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_name, 'count_document')

            if result_name_product <= 0:
                query['name_client'] = nameClient

            #if API.CountDocument(
            #    name_collection,
            #    {
            #        "_id": {"$nin" : [{ "$oid": idObject }]},
            #        'name_client': nameClient,
            #    },
            #    None,
            #    None
            #) == None:
            #    query['name_client'] = nameClient

            #if collection.count_documents({'_id': ObjectId(idObject), 'name_client': nameClient}, limit = 1) <= 0:
            #    query['name_client'] = nameClient

            #id_client
            query_count_document_id = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idObject + "')",
                        'id_client': idClient,
                    },
                
                "skip": "None",
                "limit": "None"
            }
            result_id_client = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_id, 'count_document')

            if result_id_client <= 0:
                query['id_client'] = idClient


            query_count_document_phone = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idObject + "')",
                        'phone_client': phoneClient,
                    },
                
                "skip": "None",
                "limit": "None"
            }
            result_phone = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_phone, 'count_document')

            if result_id_client <= 0:
                query['id_client'] = idClient

            #if API.CountDocument(
            #    name_collection,
            #    {
            #        "_id": {"$nin" : [{ "$oid": idObject }]},
            #        'id_client': idClient,
            #    },
            #    None,
            #    None
            #) == None:
            #    query['id_client'] = idClient
                
            #if collection.count_documents({'_id': ObjectId(idObject), 'id_client': idClient}, limit = 1) <= 0:
            #    query['id_client'] = idClient

            #phone_client
            if result_phone <= 0:
                query['phone_client'] = phoneClient

            #if API.CountDocument(
            #    name_collection,
            #    {
            #        "_id": {"$nin" : [{ "$oid": idObject }]},
            #        'phone_client': phoneClient,
            #    },
            #    None,
            #    None
            #) == None:
            #    query['phone_client'] = phoneClient
                
            #if collection.count_documents({'_id': ObjectId(idObject), 'phone_client': phoneClient}, limit = 1) <= 0:
            #    query['phone_client'] = phoneClient

            #Si no tiene items el query (no hay datos nuevos), regresar si hacer cambios  a la base de datos
            if len(query) == 0:
                return ', los datos escritos no han cambiado.'
            else:
                #collection.update_one({'_id': ObjectId(idObject)},{'$set': query })
                
                #result = API.UpdateOne(
                #    name_collection,
                #    {'_id': {'$oid': idObject}},
                #    query
                #)

                query_update_one = {
                    #nombre de la coleccion
                    "collection_choose": name_collection, 
                    #archivo a buscar
                    "search_query": 
                        {
                            "_id": "ObjectId('" + idObject + "')"
                        },
                    #dato a cambiar
                    "update_query":
                        {"$set":
                            query,
                        }
                }

                result = functions.FunctionsKivys.GetResultFromDatabase(query_update_one, 'update_one')
                return result

    def DeleteClient(id):

        #collection = DataBase.db['clients']
        #query = {'state_client': 0}

        #result = API.UpdateOne(
        #            name_collection,
        #            {'_id': {'$oid': id}},
        #            query
        #        )
        
        query_update = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": "ObjectId('" + id + "')"
                },
            #dato a cambiar
            "update_query":
                {"$set":
                    {'state_client': 0}
                }
        }

        result = functions.FunctionsKivys.GetResultFromDatabase(query_update, 'update_one')
        
        return result

        #collection.update_one({'_id': id},{'$set': query })

    def SearchUser(id):
        #collection = DataBase.db['clients']

        #result = collection.find_one({'_id': ObjectId(id)})
        
        #result = API.FindOne(
        #    name_collection,
        #    {"_id": { "$oid": id }},
        #    None
        #)
        #return result
    
        query_find_one = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": "ObjectId('" + id + "')"               
                },
            #dato a mostrar
            "projection": "None",
        }

        result = functions.FunctionsKivys.GetResultFromDatabase(query_find_one, 'find_one')

        return result