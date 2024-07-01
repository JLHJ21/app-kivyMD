import database.database as DataBase
from pymongo import ASCENDING
#from bson import ObjectId
from datetime import datetime
import MVC.controller.functions as functions

name_collection = 'products'
#API = DataBase.DatabaseClass

class CashierDB():

    def ShowDataCashierProductsModel(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        #collection = DataBase.db['products']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        #starting_id = collection.find({'state_product': 1, 'amount_product': {"$ne" : "0"}})

        #starting_id = API.Find(
        #    name_collection,
        #    {'state_product': 1, 'amount_product': {"$ne" : "0"}},
        #    {'_id': 1},
        #    None,
        #    None,
        #    {'id': -1}
        #)

        query = {
            "collection_choose": name_collection, 
            "search_query":
                {'state_product': 1, 'amount_product': {"$ne" : "0"}},
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
            #results = collection.find({'state_product': 1, 'amount_product': {"$ne" : "0"}}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1}).skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})

            #results = API.Find(
            #    name_collection, 
            #    {'state_product': 1, 'amount_product': {"$ne" : "0"}},
            #    {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1},
            #    start, 
            #    end, 
            #    {'_id': 1}
            #)

            query_find = {
                "collection_choose": name_collection, 
                "search_query":
                    {'state_product': 1, 'amount_product': {"$ne" : "0"}},
                "projection": 
                    {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1},
                "skip": start,
                "limit": end,
                "sort": "None"
            }
            
            #OBTIENE LOS DATOS DE LA COLECCION
            results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')
            #cantidad de productos que se encontraron
            #amount_items = collection.count_documents({'state_product': 1, 'amount_product': {"$ne" : "0"}}, skip=start, limit=end)
            
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

            #amount_items = API.CountDocument(
            #    name_collection,
            #    {'state_product': 1, 'amount_product': {"$ne" : "0"}},
            #    start,
            #    end
            #)
            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':

                #results = collection.find({'_id': {'$gt': last_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1} ).limit( end )#.sort({ '_id' : ObjectId(last_id)})
                
                #results = API.Find(
                #    name_collection, 
                #    {'_id': {'$gt': last_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}},
                #    {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1},
                #    None, 
                #    end, 
                #    None
                #)

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
                    "projection": 
                        {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1},
                    "skip": "None",
                    "limit": end,
                    "sort": "None"
                }

                results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

                #amount_items = API.CountDocument(
                #    name_collection,
                #    {'_id': {'$gt': last_id}, 'state_product': 1,  'amount_product': {"$ne" : "0"}},
                #    None,
                #    end
                #)

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

                #amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_product': 1,  'amount_product': {"$ne" : "0"}}, limit=end)
                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':
                #results = collection.find({'_id': {'$gte': previous_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})
                
                #results = API.Find(
                #    name_collection, 
                #    {'_id': {'$gte': previous_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}},
                #    {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1},
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
                                 
                            'state_product': 1,
                            'amount_product': {"$ne" : "0"}
                        },
                    "projection": 
                        {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1},
                    "skip": "None",
                    "limit": end,
                    "sort": "None"
                }

                results = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

                #amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, limit=end)
                #amount_items = API.CountDocument(
                #    name_collection,
                #    {'_id': {'$gte': previous_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}},
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
        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        #numbers_collection = collection.count_documents({'state_product': 1, 'amount_product': {"$ne" : "0"}})#, skip=start, limit=end)
        #numbers_collection = API.CountDocument(
        #            name_collection,
        #            {'state_product': 1, 'amount_product': {"$ne" : "0"}},
        #            None,
        #            None
        #        )
        
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

    def GetDataProduct(idProduct):
        #collection = DataBase.db['products']

        query_find_one = {
            #nombre de la coleccion
            "collection_choose": name_collection, 
            #archivo a buscar
            "search_query": 
                {
                    "_id": "ObjectId('" + idProduct + "')"
                },
            #dato a mostrar
            "projection": {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1}
        }

        results_items = functions.FunctionsKivys.GetResultFromDatabase(query_find_one, 'find_one')

        #results_items  = API.FindOne(
        #        'products',
        #        {'_id': {'$oid': idProduct}},
        #        {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1}
        #    )

        #results_items = collection.find_one({'_id': ObjectId(idProduct), 'state_product': 1}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1})
        return results_items

    def SearchClient(self, textIdClient):

        list_variables = []

        #collection = DataBase.db['clients']
        query_count_document = {
            #nombre de la coleccion
            "collection_choose": "clients", 
            #archivo a buscar
            "search_query": 
                {
                    'id_client': textIdClient, 
                    'state_client': 1
                },
            "skip": "None",
            "limit": "None"
        }

        results_items = functions.FunctionsKivys.GetResultFromDatabase(query_count_document, 'count_document')

        #results_items = API.CountDocument(
        #            'clients',
        #            {'id_client': textIdClient, 'state_client': 1},
        #            None,
        #            None
        #        )
        
        #results_items = collection.count_documents({'id_client': textIdClient, 'state_client': 1})


        if results_items >= 1:

            query_find_one = {
                #nombre de la coleccion
                "collection_choose": "clients", 
                #archivo a buscar
                "search_query": 
                    {
                        "id_client": textIdClient,
                        "state_client": 1
                    },
                #dato a mostrar
                "projection": {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1}
            }

            results = functions.FunctionsKivys.GetResultFromDatabase(query_find_one, 'find_one')

            #results = API.FindOne(
            #        'products',
            #        {'id_client': {'$oid': textIdClient}, 'state_client': 1},
            #        {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1}
            #    )
            #results = collection.find_one({'id_client': textIdClient, 'state_client': 1}, {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1})

            list_variables.append(True)
            list_variables.append(results)

        else:
            list_variables.append(False)

        return list_variables
    
    def CreateClient(nameClient, idClient, phoneClient):
        #collection = DataBase.db['clients']

        #document = {'name_client': nameClient, 'id_client': idClient, 'phone_client': phoneClient, 'state_client': 1}

        query_insert_into = {
            #nombre de la colección
            "collection_choose": name_collection, 
            #datos a agregar en la coleccion
            "document_insert":
                    {
                        'name_client': nameClient, 
                        'id_client': idClient, 
                        'phone_client': phoneClient, 
                        'state_client': 1
                    }
            }
        
        functions.FunctionsKivys.GetResultFromDatabase(query_insert_into, 'insert_into')


        #API.InsertInto(
        #        name_collection, 
        #        document
        #    )
        
        #collection.insert_one(query)

        #resultID = API.Find(
        #    name_collection,
        #    {},
        #    {'_id': 1},
        #    None,
        #    None,
        #    {'_id': -1}
        #)

        query_find = {
            "collection_choose": name_collection, 
            "search_query": "None",
            "projection": {'_id': 1},
            "skip": 0,
            "limit": 0,
            "sort": {"_id": -1}
        }

        resultID = functions.FunctionsKivys.GetResultFromDatabase(query_find, 'find')

        #resultID = collection.find_one({}, {'_id': 1}, sort= {'_id': -1})
        return resultID
    
    def UpdateAmountProduct(idProduct, amountProduct):
        
        #collection = DataBase.db['products']
        #document = {'amount_product': amountProduct}

        query_update_one = {
                #nombre de la coleccion
                "collection_choose": name_collection, 
                #archivo a buscar
                "search_query": 
                    {
                        "_id": "ObjectId('" + idProduct + "')"
                    },
                #dato a cambiar
                "update_query":
                    {"$set":
                        {'amount_product': amountProduct}
                    }
            }

        functions.FunctionsKivys.GetResultFromDatabase(query_update_one, 'update_one')

        #API.UpdateOne(
        #            name_collection,
        #            {'_id': {'$oid': idProduct}},
        #            document
        #        )

        #collection.update_one({'_id': ObjectId(idProduct)},{'$set': query })

    def AddPurchase(idObjectClient, nameClient, phoneClient, idClient, idStaff, nameStaff, purchaseAmount, typeForeignExchange, itemsProducts, purchaseAmountOriginal):
        #collection = DataBase.db['sales']
        datePurchase = datetime.today().strftime('%d-%m-%Y %H:%M:%S')

        key_products = list(itemsProducts.keys())

        products = []

        for item in (key_products)[1:]:

            dictionaryItem = {
                #identificar _id del producto
                'id_product': itemsProducts[item][0]['_id'],
                #nombre del producto
                'name_product': itemsProducts[item][0]['name_product'],
                #cantidad deseada
                'amount_wanted': itemsProducts[item][0]['amount_wanted'],
                #cantidad original del producto antes de la compra
                'amount_original': itemsProducts[item][0]['amount_original'],
                'price_product_unit': itemsProducts[item][0]['price_product_unit'],
                #precio del producto, teniendo en cuenta los datos de amount_wanted
                'total_price': itemsProducts[item][0]['total_price'],
                
            }
            products.append(dictionaryItem)

        '''
        document = {
                'data_client_sales': {
                        '_id_client': ObjectId(idObjectClient), 
                        'name_client': nameClient, 
                        'phone_client': phoneClient, 
                        'id_client': idClient
                    }, 
                'data_staff_sales': {
                        '_id_staff': ObjectId(idStaff), 
                        'name_staff': nameStaff
                    }, 
                'data_money_sales': [
                        {
                            'type_money': typeForeignExchange,
                            'purchase_money': str(purchaseAmount),
                        }
                ],
                #'purchase_amount': str(purchaseAmount), en pesos
                'total_purchase_sales': str(purchaseAmountOriginal),
                'date_sales': datePurchase, 
                #'type_money': typeForeignExchange,
                'products_sales': products, 
                'state_sales': 1
            }
        '''

        query_insert_into = {
            #nombre de la colección
            "collection_choose": "sales", 
            #datos a agregar en la coleccion
            "document_insert":
                    {
                        "data_client_sales": [
                                {
                                    "_id_client": "ObjectId('" + idObjectClient + "')",
                                    "name_client": nameClient, 
                                    "phone_client": phoneClient, 
                                    "id_client": idClient
                                }
                            ], 
                        "data_staff_sales": [
                                {
                                    "_id_staff": "ObjectId('" + idStaff + "')",
                                    "name_staff": nameStaff
                                }
                            ], 
                        "data_money_sales": [
                                {
                                    "type_money": typeForeignExchange,
                                    "purchase_money": str(purchaseAmount),
                                }
                        ],
                        #"purchase_amount": str(purchaseAmount), en pesos
                        "total_purchase_sales": str(purchaseAmountOriginal),
                        "date_sales": datePurchase, 
                        #"type_money": typeForeignExchange,
                        "products_sales": products, 
                        "state_sales": 1
                    }
            }
        
        functions.FunctionsKivys.GetResultFromDatabase(query_insert_into, 'insert_into')

        #API.InsertInto(
        #        'sales', 
        #        document
        #    )

        #collection.insert_one(post)
        