import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId
import MVC.controller.functions as functions

last_id = previous_id = None

name_collection = 'supplier'
#API = DataBase.DatabaseClass
class SupplierDB():



    def ShowData(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        #starting_id = collection.find({'state_supplier': 1})

        '''
        starting_id = API.Find(
            name_collection,
            {'state_supplier': 1},
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
                    "state_supplier": 1
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
            #results = collection.find({'state_supplier': 1}, {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1}).skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})
            
            '''
            results = API.Find(
                name_collection, 
                {'state_supplier': 1},
                {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1},
                start, 
                end, 
                {'_id': 1}
            )
            '''
            
            query_find = {
                "collection_choose": name_collection, 
                "search_query":
                    {
                        "state_supplier": 1
                    },
                "projection": {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1},
                "skip": start,
                "limit": end,
                "sort": "None"
            }

            results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

            #amount_items = collection.count_documents({'state_supplier': 1}, skip=start, limit=end)
            '''
            amount_items = API.CountDocument(
                name_collection,
                {'state_supplier': 1},
                start,
                end
            )
            '''
            query_count = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {'state_supplier': 1},
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
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_supplier': 1},
                    {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1},
                    None, 
                    end, 
                    None
                )
                '''

                #results = collection.find({'_id': {'$gt': last_id}, 'state_supplier': 1}, {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                query_find = {
                    "collection_choose": name_collection, 
                    "search_query":
                        {
                            "_id": 
                                {"$gt": 
                                    "ObjectId('" + last_id + "')"
                                }, 
                            "state_supplier": 1
                        },
                    "projection": {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1},
                    "skip": "None",
                    "limit": end,
                    "sort": "None"
                }

                results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')



                '''
                amount_items = API.CountDocument(
                    name_collection,
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_supplier': 1},
                    None,
                    end
                )
                '''
                #amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_supplier': 1}, limit=end)

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
                            "state_supplier": 1,
                            "skip": "None",
                            "limit": end
                        }
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
                    {'_id': {'$gte': { "$oid": previous_id}}, 'state_supplier': 1},
                    {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1},
                    None, 
                    end, 
                    None
                )
                '''

                #results = collection.find({'_id': {'$gte': previous_id}, 'state_supplier': 1}, {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                query_find = {
                    "collection_choose": name_collection, 
                    "search_query":
                        {
                            "_id": 
                                {
                                    '$gte': "ObjectId('" + previous_id + "')"  
                                }, 
                                 
                            "state_supplier": 1
                        },
                    "projection": {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1},
                    "skip": "None",
                    "limit": end,
                    "sort": "None"
                }

                results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

                #amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_supplier': 1}, limit=end)
                
                #amount_items = API.CountDocument(
                #    name_collection,
                #    {'_id': {'$gte': {"$oid": previous_id }}, 'state_supplier': 1},
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
                        'state_supplier': 1},

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
        
        #numbers_collection = collection.count_documents({'state_supplier': 1})#, skip=start, limit=end)
        
        #numbers_collection = API.CountDocument(
        #            name_collection,
        #            {'state_supplier': 1},
        #            None,
        #            None
        #        )
        
        query_count = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {'state_supplier': 1},
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
            d = {f"dato{index}": [i]}

            list_results.update(d)

        #RETORNA LA INFORMACIÓN OBTENIDO
        return list_results


    def CreateSupplier(name, address, rif, phone):
            
        #collection = DataBase.db['supplier']

        #data

        query_count_document_name = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    'name_supplier': name,
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_name_product = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_name, 'count_document')


        query_count_document_rif = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    'rif_supplier': rif,
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_rif = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_rif, 'count_document')


        query_count_document_phone = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    'phone_supplier': phone,
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_phone = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_phone, 'count_document')


        if result_name_product >= 1:
            return 'ya existe un nombre así'

            '''
            if API.CountDocument(
                name_collection,
                {
                    'name_supplier': name,
                },
                None,
                None
            ):
                return 'ya existe un nombre así'
            '''
        #if collection.count_documents({'name_supplier': name}, limit = 1):
        #    return 'ya existe un nombre así'

        #elif collection.count_documents({'address': address}, limit = 1):
        #    return 'address: ' + str(collection.find({'address': address}))
        
        elif result_rif >= 1:
            return 'ya existe un RIF así'

            '''
            elif API.CountDocument(
                name_collection,
                {
                    'rif_supplier': rif,
                },
                None,
                None
            ):
                return 'ya existe un RIF así'
            '''
            #elif collection.count_documents({'rif_supplier': rif}, limit = 1):
            #    return 'ya existe un RIF así'
        elif result_phone >= 1:
            return 'ya existe un teléfono así'
            '''
            elif API.CountDocument(
                name_collection,
                {
                    'phone_supplier': phone,
                },
                None,
                None
            ):
                return 'ya existe un teléfono así'
            '''

        #elif collection.count_documents({'phone_supplier': phone}, limit = 1):
        #    return 'ya existe un teléfono así'
        
        else:
            query_insert_into = {
                #nombre de la colección
                "collection_choose": name_collection, 
                #datos a agregar en la coleccion
                "document_insert":
                        {
                            'name_supplier': name, 
                            'address_supplier': address, 
                            'rif_supplier': rif, 
                            'phone_supplier': phone, 
                            'state_supplier': 1
                        },
                }
            
            result = functions.FunctionsKivys.GetResultFromDatabase(query_insert_into, 'insert_into')

            return result

            '''
            API.InsertInto(
                name_collection, 
                document
            )
            '''

        
    def UpdateSupplier(nameSupplier, addressSupplier, rifSupplier, phoneSupplier, idObject):
        
        query = {}
        #collection = DataBase.db['supplier']

        #Revisa si el dato existe en otros proveedores

        query_count_name_supplier = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": {"$nin" : [ "ObjectId('" + idObject + "')" ]},
                    "name_supplier": nameSupplier,
                    "state_supplier": 1
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_name_supplier = functions.FunctionsKivys.GetResultFromDatabase(query_count_name_supplier, 'count_document')

        query_count_direction = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": {"$nin" : [ "ObjectId('" + idObject + "')" ]},
                    'address_supplier': addressSupplier,
                    "state_supplier": 1
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_direction = functions.FunctionsKivys.GetResultFromDatabase(query_count_direction, 'count_document')

        query_count_rif = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": {"$nin" : [ "ObjectId('" + idObject + "')" ]},
                    'rif_supplier': rifSupplier,
                    "state_supplier": 1
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_rif = functions.FunctionsKivys.GetResultFromDatabase(query_count_rif, 'count_document')


        query_count_phone = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": {"$nin" : [ "ObjectId('" + idObject + "')" ]},
                    'phone_supplier': phoneSupplier,
                    "state_supplier": 1
                },
            
            "skip": "None",
            "limit": "None"
        }
        result_phone = functions.FunctionsKivys.GetResultFromDatabase(query_count_phone, 'count_document')

        if result_name_supplier >= 1:
            return ', ya existe registrado este nombre.'

        #if API.CountDocument(
        #        name_collection,
        #        {
        #            "_id": {"$nin" : [{ "$oid": idObject }]},
        #            "name_supplier": nameSupplier,
        #            "state_supplier": 1
        #        },
        #        None,
        #        None
        #    ):
        #    return ', ya existe registrado este nombre.'
        #if collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        "name_supplier": nameSupplier,
        #        "state_supplier": 1
        #    }):
        #    return ', ya existe registrado este nombre.'
        elif result_direction >= 1:
            return ', ya existe registrado esta dirección.'
            '''
            elif API.CountDocument(
                    name_collection,
                    {
                        "_id": {"$nin" : [{ "$oid": idObject }]},
                        'address_supplier': addressSupplier,
                        "state_supplier": 1
                    },
                    None,
                    None
                ):
                return ', ya existe registrado esta dirección.'
            '''
        #elif collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        'address_supplier': addressSupplier,
        #        "state_supplier": 1
        #    }):
        #    return ', ya existe registrado esta dirección.'
        elif result_rif >= 1:
            return ', ya existe registrado este RIF.'

            '''
            elif API.CountDocument(
                    name_collection,
                    {
                        "_id": {"$nin" : [{ "$oid": idObject }]},
                        'rif_supplier': rifSupplier,
                        "state_supplier": 1
                    },
                    None,
                    None
                ):
                return ', ya existe registrado este RIF.'
            '''

            #elif collection.count_documents( {
            #        "_id":  {"$nin" : [ObjectId(idObject)]},
            #        'rif_supplier': rifSupplier,
            #        "state_supplier": 1
            #    }):
            #    return ', ya existe registrado este RIF.'
    
        elif result_phone >= 1:
            return ', ya existe registrado este número de teléfono.'
        
            '''
            elif API.CountDocument(
                    name_collection,
                    {
                        "_id": {"$nin" : [{ "$oid": idObject }]},
                        'phone_supplier': phoneSupplier,
                        "state_supplier": 1
                    },
                    None,
                    None
                ):
                return ', ya existe registrado este número de teléfono.'
            '''
            #elif collection.count_documents( {
            #        "_id":  {"$nin" : [ObjectId(idObject)]},
            #        'phone_supplier': phoneSupplier,
            #        "state_supplier": 1
            #    }):
            #    return ', ya existe registrado este número de teléfono.'

        else:
            #data
            ####Si no es el mismo el dato introducido anteriormente, lo añade al query
            #name_supplier

            query_count_document_name_supplier = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idObject + "')",
                        'name_supplier': nameSupplier,
                    },
                
                "skip": "None",
                "limit": "None"
            }

            result_name_supplier = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_name_supplier, 'count_document')

            #address
            query_count_document_address = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idObject + "')",
                        'address_supplier': addressSupplier,
                    },
                
                "skip": "None",
                "limit": "None"
            }

            result_address = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_address, 'count_document')

            #rif
            query_count_document_rif = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idObject + "')",
                        'rif_supplier': rifSupplier,
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
                        "_id": "ObjectId('" + idObject + "')",
                        'phone_supplier': phoneSupplier,
                    },
                
                "skip": "None",
                "limit": "None"
            }

            result_phone = functions.FunctionsKivys.GetResultFromDatabase(query_count_document_phone, 'count_document')

            if result_name_supplier <= 0:
                query['name_supplier'] = nameSupplier

                '''
                if API.CountDocument(
                    name_collection,
                    {
                        "_id": {"$nin" : [{ "$oid": idObject }]},
                        'name_supplier': nameSupplier,
                    },
                    None,
                    None
                ) == None:
                    query['name_supplier'] = nameSupplier
                #if collection.count_documents({'_id': ObjectId(idObject), 'name_supplier': nameSupplier}, limit = 1) <= 0:
                #    query['name_supplier'] = nameSupplier
                '''
            #address_supplier
            elif result_address <= 0:
                query['address_supplier'] = addressSupplier

                '''
                elif API.CountDocument(
                    name_collection,
                    {
                        "_id": {"$nin" : [{ "$oid": idObject }]},
                        'address_supplier': addressSupplier,
                    },
                    None,
                    None
                ) == None:
                    query['address_supplier'] = addressSupplier
                '''
                #if collection.count_documents({'_id': ObjectId(idObject), 'address_supplier': addressSupplier}, limit = 1) <= 0:
                #    query['address_supplier'] = addressSupplier

            #rif_supplier
            elif result_rif <= 0:
                query['rif_supplier'] = rifSupplier

                '''
                elif API.CountDocument(
                    name_collection,
                    {
                        "_id": {"$nin" : [{ "$oid": idObject }]},
                        'rif_supplier': rifSupplier,
                    },
                    None,
                    None
                ) == None:
                    query['rif_supplier'] = rifSupplier
                '''
            #if collection.count_documents({'_id': ObjectId(idObject), 'rif_supplier': rifSupplier}, limit = 1) <= 0:
            #    query['rif_supplier'] = rifSupplier

            #phone_supplier
            elif result_phone <= 0:
                query['phone_supplier'] = phoneSupplier

                '''
                elif API.CountDocument(
                    name_collection,
                    {
                        "_id": {"$nin" : [{ "$oid": idObject }]},
                        'phone_supplier': phoneSupplier,
                    },
                    None,
                    None
                ) == None:
                    query['phone_supplier'] = phoneSupplier
                '''
            #if collection.count_documents({'_id': ObjectId(idObject), 'phone_supplier': phoneSupplier}, limit = 1) <= 0:
            #    query['phone_supplier'] = phoneSupplier

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
                #return True
    
    def DeleteSupplier(id):

        query_aggregate_charges = {
            #nombre de la coleccion
            "collection_choose": "charges", 
            #archivo a buscar
            "search_query": 
                {
                    "id_supplier": "ObjectId('" + id + "')"
                },
            #cantidad de resultados
            "limit": "None",
            #aggregate a realizar, puede ser para obtener datos de arrays como contarlos
            "projection": { '_id': 0, 'products_sales.id_product' : 1 , 'products_sales.amount_wanted' : 1 }
        }

        results_charges = functions.FunctionsKivys.GetResultFromDatabase(query_aggregate_charges, 'aggregate')


        #results_charges = API.Aggregate(
        #    'charges',
        #    { 'id_supplier': {'$oid': id} },
        #    None,
        #    1,
        #    { '_id': 1, 'products.id_product' : 1 , 'products.amount_product' : 1 } 
        #)

        #results_charges = collection_charges.aggregate([
        #    { '$match': { 'id_supplier': id } },
        #    { '$limit': 1},
        #    { '$project' : 
        #        { '_id':0, 'products.id_product' : 1 , 'products.amount_product' : 1 } 
        #    }
        
        #])

        list_results_charges = list(results_charges)

        if len(list_results_charges) > 0:

            for item in list_results_charges[0]['products']:
                
                #result_product = collection_products.find_one({'_id': item['id_product']})

                #result_product = API.FindOne(
                #    'products',
                #    {'_id': {'$oid': item['id_product']}},
                #    None
                #)

                query_find_one = {
                    #nombre de la coleccion
                    "collection_choose": 'products', 
                    #archivo a buscar
                    "search_query": 
                        {
                            "_id": "ObjectId('" + item['id_product'] + "')"               
                        },
                    #dato a mostrar
                    "projection": "None",
                }

                result_product = functions.FunctionsKivys.GetResultFromDatabase(query_find_one, 'find_one')


                if result_product:

                    amount_actual = int(result_product['amount_product']) - int(item['amount_product']) 

                    if amount_actual > 0:

                        query_update_one = {
                            #nombre de la coleccion
                            "collection_choose": "products", 
                            #archivo a buscar
                            "search_query": 
                                {
                                    "_id": "ObjectId('" + item['id_product'] + "')"
                                },
                            #dato a cambiar
                            "update_query":
                                {"$set":
                                    {'amount_product': str(amount_actual)},
                                }
                        }

                        functions.FunctionsKivys.GetResultFromDatabase(query_update_one, 'update_one')

                        #API.UpdateOne(
                        #    'products',
                        #    { '_id': {'$oid': item['id_product']} },
                        #    query
                        #)

                        #collection_products.update_one({'_id': item['id_product']},{'$set': query })
                    else:
                        
                        #collection_products.update_one({'_id': item['id_product']},{'$set': query })

                        query_update_one = {
                            #nombre de la coleccion
                            "collection_choose": "products", 
                            #archivo a buscar
                            "search_query": 
                                {
                                    "_id": "ObjectId('" + item['id_product'] + "')"
                                },
                            #dato a cambiar
                            "update_query":
                                {"$set":
                                    {'state_product': 2},
                                }
                        }

                        functions.FunctionsKivys.GetResultFromDatabase(query_update_one, 'update_one')

                        #API.UpdateOne(
                        #    'products',
                        #    { '_id': {'$oid': item['id_product']} },
                        #    query
                        #)

        #collection.update_one({'_id': id},{'$set': query })
        #query = {'state_supplier': 0}

        #API.UpdateOne(
        #    name_collection,
        #    { '_id': {'$oid': id} },
        #    query
        #)

        query_update_one = {
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
                    {'state_supplier': 0},
                }
        }

        functions.FunctionsKivys.GetResultFromDatabase(query_update_one, 'update_one')


        

    def SearchSupplier(id):
        #collection = DataBase.db['supplier']

        #result = collection.find_one({'_id': ObjectId(id)})
        
        #result = API.FindOne(
        #    name_collection,
        #    {"_id": { "$oid": id }},
        #    None
        #)

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