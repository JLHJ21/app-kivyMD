import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId
from datetime import datetime
import re

last_id = previous_id = None

class ChargesDB():



    def ShowDataChargesModel(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        collection = DataBase.db['charges']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        starting_id = collection.find({'state_charges': 1})

        #SI EL ESTADO ES NONE, REINICIA LAS VARIABLES GLOBALES
        if state == '':
            last_id = previous_id = None

        #SE ACTIVA AL SER LA PRIMERA LLAMADA A LA BASE DE DATOS
        if last_id == None:


            #OBTIENE LOS DATOS DE LA COLECCION
            results = collection.find({'state_charges': 1}, {'_id': 1, 'name_supplier': 1, 'buy_products': 1, 'date': 1}).skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})
            
            #cantidad de productos que se encontraron
            amount_items = collection.count_documents({'state_charges': 1}, skip=start, limit=end)

            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']


        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':

                results = collection.find({'_id': {'$gt': last_id}, 'state_charges': 1}, {'_id': 1, 'name_supplier': 1, 'buy_products': 1, 'date': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_charges': 1}, limit=end)
                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':

                results = collection.find({'_id': {'$gte': previous_id}, 'state_charges': 1}, {'_id': 1, 'name_supplier': 1, 'buy_products': 1, 'date': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_charges': 1}, limit=end)
                
                #OBTIENE EL ULTIMO ID DEL ITEM DE LA COLECCION
                last_id = results[amount_items - 1]['_id']

                if (start - end) - 1 < 0:
            
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

        #SE CREA DICCIONARIO QUE ALMACENARÁ LOS DATOS OBTENIDOS DE LA BASE DE DATOS
        list_results = {}
        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        numbers_collection = collection.count_documents({'state_charges': 1})#, skip=start, limit=end)

        #SE AGREGA SIEMPRE COMO PRIMER DATO, LAS CARACTERISTICAS (CANTIDAD DE DOCUMENTOS, ARCHIVO COMIENZA, ARCHIVO TERMINADA)
        list_results.update({'characteristics': [numbers_collection, start, end]})

        
        #CICLO FOR QUE AGREGA LOS DATOS OBTENIDO DE LA BASE DE DATOS AL DICCIONARIO LIST_RESULTS, ESTO HACE QUE LA VARIABLE RESULTS(CURSOR) SE VACIE 

        for index, i in enumerate(results):

            #LO ALMACENA DE FORMA, DATO(POSICION): 'TODA LA INFORMACIÓN DE LA BASE DE DATOS
            d = {f"dato{index}": [i]}

            list_results.update(d)


        for index, result in enumerate(list_results):
            try:
                amount_item =  ChargesDB.GetAmountItemsCharge(collection, list_results[result][0]['_id'])
                
                dictionary_item = {'products': str(amount_item)}
                list_results[result][0].update(dictionary_item)
                
            except:
                pass
            
        return list_results
    
    def GetAmountItemsCharge(collection, id_charges):
        pipeline = [
            {
            '$match': {
                    '_id': id_charges #results_amount_item[0]['name_supplier']
                }
            },
            {
                "$unwind": "$products" # descompone el array en un documento por separado
            },
            {
                '$group': {
                    '_id': "$products.name_product", # agrupamos por el tags
                    'count': {
                    '$sum': 1 # Realizamos sumatoria
                    }
                }
            }
        ]

        result = len(list(collection.aggregate( pipeline )))
        return result

    def GetDataSupplier(text):

        rgx = re.compile('.*'+ text +'.*', re.IGNORECASE)  # compile the regex


        collection = DataBase.db['supplier']

        results = collection.find({'name_supplier': rgx , 'state_supplier': 1}, {'name_supplier': 1}).limit( 5 )#.sort({ '_id' : ObjectId(last_id)})

        #SE CREA DICCIONARIO QUE ALMACENARÁ LOS DATOS OBTENIDOS DE LA BASE DE DATOS
        list_results = {}

        #CICLO FOR QUE AGREGA LOS DATOS OBTENIDO DE LA BASE DE DATOS AL DICCIONARIO LIST_RESULTS, ESTO HACE QUE LA VARIABLE RESULTS(CURSOR) SE VACIE 
        for index, i in enumerate(results):

            #LO ALMACENA DE FORMA, DATO(POSICION): 'TODA LA INFORMACIÓN DE LA BASE DE DATOS
            d = {f"dato{index}": i}

            list_results.update(d)

        

        #RETORNA LA INFORMACIÓN OBTENIDO
        return list_results

    def InsertNewCharge(new_product, name_product, amount_product, buy_product, profit_product, name_supplier, id_supplier, money_buys, money_profits, money_total):
        
        #CONEXION A LA COLECCION
        collection = DataBase.db['charges']
        collection_products = DataBase.db['products']
        collection_supplier = DataBase.db['supplier']


        date = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        list_ids_products = []

        result_supplier = collection_supplier.count_documents({'name_supplier': name_supplier, 'state_supplier': 1}, limit = 1)

        if result_supplier > 0:
                
            #agregar/modificarlo producto
            for index, item in enumerate(name_product):

                #Si es nuevo el producto lo agrega
                if new_product[index] == False:
                    #query
                    post = {'name_product': item, 'amount_product': str(amount_product[index]), 'buy_product': str(buy_product[index]), 'profit_product': str(profit_product[index]), 'name_supplier': name_supplier, 'state_product': 1}

                    #insertar
                    collection_products.insert_one(post)
                    list_ids_products.append(list(collection_products.find({}, {'_id': 1}).sort({'_id':-1}).limit(1) ))
                #Si es viejo, revisa que datos ha cambiado
                else:
                    #datos del producto ya existente
                    results = collection_products.find_one({'name_product': item, 'state_product': 1}, {'_id': 1, 'amount_product': 1, 'buy_product': 1, 'profit_product': 1, 'name_supplier': 1})
                
                    new_amount = int(results['amount_product']) + int(amount_product[index])
                    new_buy = float(buy_product[index])
                    new_profit = float(profit_product[index])


                    if results['name_supplier'] == name_supplier:
                        query = {'amount_product': str(new_amount), 'buy_product': str(new_buy), 'profit_product': str(new_profit)}

                    else:
                        new_supplier = name_supplier

                        query = {'amount_product': str(new_amount), 'buy_product': str(new_buy), 'profit_product': str(new_profit), 'name_supplier': new_supplier}

                    collection_products.update_one({'_id': ObjectId(results['_id'])}, {'$set': query })


                    id = [{'_id': results['_id']}]
                    list_ids_products.append(id)


            products = []

            #Insertar en Charges/Encargos
            for index, item in enumerate(list_ids_products[::-1]):

                noSQL = {'name_product': name_product[index],
                    'amount_product': str(amount_product[index]),
                    'buy_product': str(buy_product[index]),
                    'profit_product': str(profit_product[index]),
                    'id_product': ObjectId(item[0]['_id'])
                }

                products.append(noSQL)


            post = {'name_supplier': name_supplier,
                'id_supplier': ObjectId(id_supplier),
                'products': products,
                'date': date,
                'buy_products': str(money_buys),
                'profit_products': str(money_profits),
                'total_money': str(money_total) ,
                'state_charges': 1
            }

            collection.insert_one(post)

            return True
        else:
            return ', no existe el proveedor que escribiste.'
    
    def ExistProduct(textProduct):
        

        #rgx = re.compile('.*'+ textProduct +'.*', re.IGNORECASE)  # compile the regex


        collection = DataBase.db['products']

        results = collection.count_documents({'name_product': textProduct})

        if results > 0:
            return True
        else:
            return False
        

        #RETORNA LA INFORMACIÓN OBTENIDO
        #return list_results