import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId


from time import sleep
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
import MVC.controller.functions as functions

last_id = previous_id = None
name_collection = 'products'
#API = DataBase.DatabaseClass

class StoreDB():

    def ShowDataStoreModel(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        #collection = DataBase.db['products']


        #OBTIENE TODOS LOS DATOS DE LA COLECCION


        #starting_id = collection.find({'state_product': 1, 'amount_product': {"$ne" : "0"}}).sort({'id': -1})

        '''
        starting_id = API.Find(
            name_collection,
            {'state_product': 1, 'amount_product': {"$ne" : "0"}},
            {'_id': 1},
            None,
            None,
            {'id': -1}
        )
        '''

        query = {
            "collection_choose": name_collection, 
            "search_query":
                {
                    'state_product': 1, 
                    'amount_product': {"$ne" : "0"}
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

            query_find = {
                "collection_choose": name_collection, 
                "search_query":
                    {'state_product': 1, 'amount_product': {"$ne" : "0"}},
                "projection": {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1},
                "skip": start,
                "limit": end,
                "sort": "None"
            }
            
            #OBTIENE LOS DATOS DE LA COLECCION
            results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

            '''
            results = API.Find(
                name_collection, 
                {'state_product': 1, 'amount_product': {"$ne" : "0"}},
                {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1},
                start, 
                end, 
                None
            )
            #results = collection.find({'state_product': 1, 'amount_product': {"$ne" : "0"}}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1}).skip(start).limit( end ) #.sort({ '_id' : -1})
            
            #cantidad de productos que se encontraron
            
            amount_items = API.CountDocument(
                name_collection,
                {'state_product': 1, 'amount_product': {"$ne" : "0"}},
                start,
                end
            )
            #amount_items = collection.count_documents({'state_product': 1, 'amount_product': {"$ne" : "0"}}, skip=start, limit=end)
            '''

            query_count = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {'state_product': 1, 'amount_product': {"$ne" : "0"}},
                "skip": start,
                "limit": end
            }

            #cantidad de productos que se encontraron
            amount_items = functions.FunctionsKivys.GetResultFromDatabase(query_count, 'count_document')


            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':

                '''
                results = API.Find(
                    name_collection, 
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_product': 1, 'amount_product': {"$ne" : "0"}},
                    {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1},
                    None, 
                    end, 
                    None
                )
                '''
                #results = collection.find({'_id': {'$gt': last_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1} ).limit( end )#.sort({ '_id' : ObjectId(last_id)})
               
                query_find = {
                    "collection_choose": name_collection, 
                    "search_query":
                        {
                            "_id": 
                                {"$gt": 
                                    "ObjectId('" + last_id + "')"
                                }, 
                            'state_product': 1, 
                            'amount_product': {"$ne" : "0"}
                        },
                    "projection": {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1},
                    "skip": "None",
                    "limit": end,
                    "sort": "None"
                }

                results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')
                '''
                amount_items = API.CountDocument(
                    name_collection,
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_product': 1, 'amount_product': {"$ne" : "0"}},
                    None,
                    end
                )
                '''

                #amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, limit=end)

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
                            'state_product': 1, 
                            'amount_product': {"$ne" : "0"}
                        },
                    "skip": "None",
                    "limit": end
                }


                amount_items = functions.FunctionsKivys.GetResultFromDatabase(query_count, 'count_document')

                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':

                '''
                results = API.Find(
                    name_collection, 
                    {'_id': {'$gte': { "$oid": previous_id}}, 'state_product': 1, 'amount_product': {"$ne" : "0"}},
                    {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1},
                    None, 
                    end, 
                    None
                )
                '''
                #results = collection.find({'_id': {'$gte': previous_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                query_find = {
                    "collection_choose": name_collection, 
                    "search_query":
                        {
                            "_id": 
                                {
                                    '$gte': "ObjectId('" + previous_id + "')"  
                                }, 
                                 
                            'state_product': 1, 
                            'amount_product': {"$ne" : "0"}
                        },
                    "projection": {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1},
                    "skip": "None",
                    "limit": end,
                    "sort": "None"
                }

                results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

                #amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, limit=end)

                '''
                amount_items = API.CountDocument(
                    name_collection,
                    {'_id': {'$gte': {"$oid": previous_id }}, 'state_product': 1, 'amount_product': {"$ne" : "0"}},
                    None,
                    end
                )
                '''
                query_count = {
                    #nombre de la coleccion
                    "collection_choose": name_collection, 
                    #archivo a buscar
                    "search_query": 
                        {'_id': 
                            {'$gte': "ObjectId('"+ previous_id +  "')"  }, 
                            'state_product': 1, 
                            'amount_product': {"$ne" : "0"}
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
        '''
        numbers_collection = API.CountDocument(
                    name_collection,
                    {'state_product': 1, 'amount_product': {"$ne" : "0"}},
                    None,
                    None
                )
        #numbers_collection = collection.count_documents({'state_product': 1, 'amount_product': {"$ne" : "0"}})#, skip=start, limit=end)
        '''
        query_count = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {'state_product': 1, 'amount_product': {"$ne" : "0"}},
            "skip": "None",
            "limit": "None"
        }

        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        numbers_collection = functions.FunctionsKivys.GetResultFromDatabase(query_count, 'count_document')

        #SE AGREGA SIEMPRE COMO PRIMER DATO, LAS CARACTERISTICAS (CANTIDAD DE DOCUMENTOS, ARCHIVO COMIENZA, ARCHIVO TERMINADA)
        list_results.update({'characteristics': [numbers_collection, start, end]})

        
        #CICLO FOR QUE AGREGA LOS DATOS OBTENIDO DE LA BASE DE DATOS AL DICCIONARIO LIST_RESULTS, ESTO HACE QUE LA VARIABLE RESULTS(CURSOR) SE VACIE 
        for index, i in enumerate(results):

            #LO ALMACENA DE FORMA, DATO(POSICION): 'TODA LA INFORMACIÓN DE LA BASE DE DATOS
            d = {f"dato{index}": [(i)]}

            list_results.update(d)

        #RETORNA LA INFORMACIÓN OBTENIDO

        return list_results

    #def UpdateProduct(nameProduct, amountProduct, profitProduct, supplierProduct, idObject):
    def UpdateProduct(nameProduct, profitProduct, supplierProduct, idObject):
        
        query = {}
        #collection = DataBase.db['products']


        #Revisa si el dato existe en otros productos
        #if collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        'name_product': nameProduct,
        #        "state_product": 1
        #    }):
        #    return ', ya existe registrado este nombre.'

        query_count_document_name = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": {"$nin" : [ "ObjectId('" + idObject + "')" ]},
                    'name_product': nameProduct,
                    "state_product": 1
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_name_product = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_name, 'count_document')

        if result_name_product >= 1:
            return ', ya existe registrado este nombre.'
            '''
            if API.CountDocument(
                    name_collection,
                    {
                        "_id": {"$nin" : [{ "$oid": idObject }]},
                        'name_product': nameProduct,
                        "state_product": 1
                    },
                    None,
                    None
                ):
                return ', ya existe registrado este nombre.'
            '''
        else:
            #data
            ####Si no existe el dato introducido, lo añade al query
            #name_product
            query_count_document_name = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idObject + "')",
                        'name_product': nameProduct,
                    },
                
                "skip": "None",
                "limit": "None"
            }
            result_name_product = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_name, 'count_document')

            if result_name_product <= 0:
                query['name_product'] = nameProduct
                '''
                if API.CountDocument(
                    name_collection,
                    {
                        "_id": {"$nin" : [{ "$oid": idObject }]},
                        'name_product': nameProduct,
                    },
                    None,
                    None
                ) == None:
                    query['name_product'] = nameProduct
                '''
                
            #if collection.count_documents({'_id': ObjectId(idObject), 'name_product': nameProduct}, limit = 1) <= 0:
            #    query['name_product'] = nameProduct

            #amount_product
            #if collection.count_documents({'_id': ObjectId(idObject), 'amount_product': amountProduct}, limit = 1) <= 0:
            #    query['amount_product'] = amountProduct

            query_count_document_profit = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idObject + "')",
                        'profit_product': profitProduct,
                    },
                
                "skip": "None",
                "limit": "None"
            }

            result_profit_product = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_profit, 'count_document')
            if result_profit_product <= 0:
                query['profit_product'] = profitProduct

            #profit_product
            '''
            if API.CountDocument(
                name_collection,
                {
                    "_id": {"$nin" : [{ "$oid": idObject }]},
                    'profit_product': profitProduct,
                },
                None,
                None
            ) == None:
                query['profit_product'] = profitProduct
            '''

            #if collection.count_documents({'_id': ObjectId(idObject), 'profit_product': profitProduct}, limit = 1) <= 0:
            #    query['profit_product'] = profitProduct

            #name_supplier
            query_count_document_name_supplier = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idObject + "')",
                        'name_supplier': supplierProduct,
                    },
                
                "skip": "None",
                "limit": "None"
            }

            result_name_supplier = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_name_supplier, 'count_document')
            if result_name_supplier <= 0:
                query['name_supplier'] = supplierProduct

            '''
            if API.CountDocument(
                name_collection,
                {
                    "_id": {"$nin" : [{ "$oid": idObject }]},
                    'name_supplier': supplierProduct,
                },
                None,
                None
            ) == None:
                query['name_supplier'] = supplierProduct
            '''
            #if collection.count_documents({'_id': ObjectId(idObject), 'name_supplier': supplierProduct}, limit = 1) <= 0:
            #    query['name_supplier'] = supplierProduct

            ##########
            #Si no tiene items el query (no hay datos nuevos), regresar si hacer cambios  a la base de datos
            if len(query) == 0:
                return ', los datos ingresados son los mismos que habia antes.'
            else:

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

                '''
                result = API.UpdateOne(
                    name_collection,
                    {'_id': {'$oid': idObject}},
                    query
                )
                '''

                #collection.update_one({'_id': ObjectId(idObject)},{'$set': query })

    
    def DeleteProduct(id):

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
                    {'state_product': 0},
                }
        }

        functions.FunctionsKivys.GetResultFromDatabase(query_update, 'update_one')

        '''
        API.UpdateOne(
            name_collection,
            {"_id": { "$oid": id }},
            {'state_product': 0}
        )
        '''
        #collection = DataBase.db['products']

        #query = {'state_product': 0}

        #collection.update_one({'_id': id},{'$set': query })

    def SearchProduct(id):
        
        #collection = DataBase.db['products']

        #result = collection.find_one({'_id': ObjectId(id)})
        '''
        result = API.FindOne(
            name_collection,
            {"_id": { "$oid": id }},
            None
        )
        
        return result
        '''
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