import database.database as DataBase
import MVC.controller.functions as functions


name_collection = 'sales'
API = DataBase.DatabaseClass

class SalesHistoryDB():
    def ShowDataSalesHistoryModel(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        collection = DataBase.db['sales']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        #starting_id = collection.find({'state_sales': 1})
        starting_id = API.Find(
            name_collection,
            {'state_sales': 1},
            {'_id': 1},
            None,
            None,
            {'id': -1}
        )

        #SI EL ESTADO ES NONE, REINICIA LAS VARIABLES GLOBALES
        if state == '':
            last_id = previous_id = None

        #SE ACTIVA AL SER LA PRIMERA LLAMADA A LA BASE DE DATOS
        if last_id == None:

            #OBTIENE LOS DATOS DE LA COLECCION
            #results = collection.find({'state_sales': 1}).skip(start).limit( end )#.sort({'_id': 1}) #.sort({ '_id' : -1})

            results = API.Find(
                name_collection, 
                {'state_sales': 1},
                None,
                start, 
                end, 
                None
            )
            #results1 = collection.find({'state_sales': 1}).skip(start).limit( end )#.sort({'_id': 1}) #.sort({ '_id' : -1})

            #cantidad de productos que se encontraron
            #amount_items = collection.count_documents({'state_sales': 1}, skip=start, limit=end)

            amount_items = API.CountDocument(
                name_collection,
                {'state_sales': 1},
                start,
                end
            )

            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':

                results = collection.find({'_id': {'$gt': last_id}, 'state_sales': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                results = API.Find(
                    name_collection, 
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_sales': 1},
                    None,
                    None, 
                    end, 
                    None
                )

                #amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_sales': 1}, limit=end)

                amount_items = API.CountDocument(
                    name_collection,
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_sales': 1},
                    None,
                    end
                )

                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':
                #results = collection.find({'_id': {'$gte': previous_id}, 'state_sales': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})
                
                results = API.Find(
                    name_collection, 
                    {'_id': {'$gte': { "$oid": previous_id}}, 'state_sales': 1},
                    None,
                    None, 
                    end, 
                    None
                )
                #amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_sales': 1}, limit=end)
                
                amount_items = API.CountDocument(
                    name_collection,
                    {'_id': {'$gte': {"$oid": previous_id }}, 'state_sales': 1},
                    None,
                    end
                )

                #OBTIENE EL ULTIMO ID DEL ITEM DE LA COLECCION
                last_id = results[amount_items - 1]['_id']

                if (start - end) - 1 < 0:
            
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

        #SE CREA DICCIONARIO QUE ALMACENARÁ LOS DATOS OBTENIDOS DE LA BASE DE DATOS
        list_results = {}
        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        #numbers_collection = collection.count_documents({'state_sales': 1})#, skip=start, limit=end)

        numbers_collection = API.CountDocument(
                    name_collection,
                    {'state_sales': 1},
                    None,
                    None
                )

        #SE AGREGA SIEMPRE COMO PRIMER DATO, LAS CARACTERISTICAS (CANTIDAD DE DOCUMENTOS, ARCHIVO COMIENZA, ARCHIVO TERMINADA)
        list_results.update({'characteristics': [numbers_collection, start, end]})

        #CICLO FOR QUE AGREGA LOS DATOS OBTENIDO DE LA BASE DE DATOS AL DICCIONARIO LIST_RESULTS, ESTO HACE QUE LA VARIABLE RESULTS(CURSOR) SE VACIE 
        

        for index, i in enumerate(results):

            #LO ALMACENA DE FORMA, DATO(POSICION): 'TODA LA INFORMACIÓN DE LA BASE DE DATOS


            idSalesHistory = i['_id']

            amount_products = SalesHistoryDB.GetAmountItemsSales(idSalesHistory)

            nameClient = i['data_client_sales']['name_client']
            nameStaff = i['data_staff_sales']['name_staff']
            totalPurchase = i['total_purchase_sales']
            datePurchase = i['date_sales']

            item_dictionary = {
                "_id": idSalesHistory,
                "name_client": nameClient,
                "name_staff": nameStaff,
                "total_purchase_sales": totalPurchase,
                "amount_products": str(amount_products),
                "date_sales": datePurchase
            }



            d = {f"dato{index}": [item_dictionary]}

            list_results.update(d)

        #RETORNA LA INFORMACIÓN OBTENIDO

        return list_results
    
    def GetAmountItemsSales(id_sales):


        #collection = DataBase.db['sales']

        '''
        pipeline = [
            '$project': {
                'productsAmount': { 
                    '$size': "$products_sales" 
                },
            },
            {
            '$match': {
                    '_id': id_sales #results_amount_item[0]['name_supplier']
                },
            },
        ]
        
        
            {
                "$unwind": "$products_sales" # descompone el array en un documento por separado
            },
            {
                '$group': {
                    '_id': "$products_sales.id_product", # agrupamos por el tags
                    'count': {
                    '$sum': 1 # Realizamos sumatoria
                    }
                }
            }
        
        '''

        result = API.Aggregate(
            'sales',
            {'_id': {'$oid': id_sales}},
            None,
            None,
            { '_id' : 0 , 'productsAmount': { '$size': "$products_sales" } },
        )

        #result = collection.aggregate(
        #    [
                
        #        {
        #        '$match': {
        #                '_id': id_sales #results_amount_item[0]['name_supplier']
        #            },
        #        },
                
        #        {
        #            '$project': {
        #                '_id' : 0 ,
        #                'productsAmount': { 
        #                    '$size': "$products_sales" 
        #                },
        #            },
        #            
        #        },
        #    ]
        # )
        


        list_result = list(result)
        return list_result[0]['productsAmount']