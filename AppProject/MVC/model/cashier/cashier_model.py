import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId
from datetime import datetime



class CashierDB():

    def ShowDataCashierProductsModel(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        collection = DataBase.db['products']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        starting_id = collection.find({'state_product': 1, 'amount_product': {"$ne" : "0"}})

        #SI EL ESTADO ES NONE, REINICIA LAS VARIABLES GLOBALES
        if state == '':
            last_id = previous_id = None

        #SE ACTIVA AL SER LA PRIMERA LLAMADA A LA BASE DE DATOS
        if last_id == None:

            #OBTIENE LOS DATOS DE LA COLECCION
            results = collection.find({'state_product': 1, 'amount_product': {"$ne" : "0"}}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1}).skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})
            
            #cantidad de productos que se encontraron
            amount_items = collection.count_documents({'state_product': 1, 'amount_product': {"$ne" : "0"}}, skip=start, limit=end)

            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':

                results = collection.find({'_id': {'$gt': last_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1} ).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_product': 1,  'amount_product': {"$ne" : "0"}}, limit=end)
                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':
                results = collection.find({'_id': {'$gte': previous_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_product': 1, 'amount_product': {"$ne" : "0"}}, limit=end)
                
                #OBTIENE EL ULTIMO ID DEL ITEM DE LA COLECCION
                last_id = results[amount_items - 1]['_id']

                if (start - end) - 1 < 0:
            
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

        #SE CREA DICCIONARIO QUE ALMACENARÁ LOS DATOS OBTENIDOS DE LA BASE DE DATOS
        list_results = {}
        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        numbers_collection = collection.count_documents({'state_product': 1, 'amount_product': {"$ne" : "0"}})#, skip=start, limit=end)

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
        collection = DataBase.db['products']
        results_items = collection.find_one({'_id': idProduct, 'state_product': 1}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1})
        return results_items

    def SearchClient(self, textIdClient):

        list_variables = []

        collection = DataBase.db['clients']
        results_items = collection.count_documents({'id_client': textIdClient, 'state_client': 1})


        if results_items >= 1:
            results = collection.find_one({'id_client': textIdClient, 'state_client': 1}, {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1})

            list_variables.append(True)
            list_variables.append(results)

        else:
            list_variables.append(False)


        return list_variables
    
    def CreateClient(nameClient, idClient, phoneClient):
        collection = DataBase.db['clients']

        query = {'name_client': nameClient, 'id_client': idClient, 'phone_client': phoneClient, 'state_client': 1}

        collection.insert_one(query)

        resultID = collection.find_one({}, {'_id': 1}, sort= {'_id': -1})
        return resultID
    
    def UpdateAmountProduct(idProduct, amountProduct):
        
        collection = DataBase.db['products']
        query = {'amount_product': amountProduct}

        collection.update_one({'_id': ObjectId(idProduct)},{'$set': query })

    def AddPurchase(idObjectClient, nameClient, phoneClient, idClient, idStaff, nameStaff, purchaseAmount, typeForeignExchange,itemsProducts):
        collection = DataBase.db['sales']
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
                #precio del producto, teniendo en cuenta los datos de amount_wanted
                'total_price': itemsProducts[item][0]['total_price'],
                
            }
            products.append(dictionaryItem)

        print('aqui')
        print(idObjectClient)
        print(type(idObjectClient))
        print()

        post = {
                'data_client': {
                        '_id_client': ObjectId(idObjectClient), 
                        'name_client': nameClient, 
                        'phone_client': phoneClient, 
                        'id_client': idClient
                    }, 
                'data_staff': {
                        '_id_staff': ObjectId(idStaff), 
                        'name_staff': nameStaff
                    }, 
                'purchase_amount': str(purchaseAmount), 
                'date_purchase': datePurchase, 
                'type_money': typeForeignExchange,
                'products': products, 
                'state_sales': 1
            }

        print('MODEL')
        print(products)
        collection.insert_one(post)
        