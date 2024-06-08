import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId

last_id = previous_id = None

class SupplierDB():



    def ShowData(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        collection = DataBase.db['supplier']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        starting_id = collection.find({'state_supplier': 1})

        #SI EL ESTADO ES NONE, REINICIA LAS VARIABLES GLOBALES
        if state == '':
            last_id = previous_id = None

        #SE ACTIVA AL SER LA PRIMERA LLAMADA A LA BASE DE DATOS
        if last_id == None:

            #OBTIENE LOS DATOS DE LA COLECCION
            results = collection.find({'state_supplier': 1}, {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1}).skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})
            
            #cantidad de productos que se encontraron
            amount_items = collection.count_documents({'state_supplier': 1}, skip=start, limit=end)

            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':
                results = collection.find({'_id': {'$gt': last_id}, 'state_supplier': 1}, {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_supplier': 1}, limit=end)
                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':
                results = collection.find({'_id': {'$gte': previous_id}, 'state_supplier': 1}, {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_supplier': 1}, limit=end)
                
                #OBTIENE EL ULTIMO ID DEL ITEM DE LA COLECCION
                last_id = results[amount_items - 1]['_id']

                if (start - end) - 1 < 0:
            
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

        #SE CREA DICCIONARIO QUE ALMACENARÁ LOS DATOS OBTENIDOS DE LA BASE DE DATOS
        list_results = {}
        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        numbers_collection = collection.count_documents({'state_supplier': 1})#, skip=start, limit=end)

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
            
        collection = DataBase.db['supplier']

        #data

        if collection.count_documents({'name_supplier': name}, limit = 1):

            return 'ya existe un nombre así'

        #elif collection.count_documents({'address': address}, limit = 1):
        #    return 'address: ' + str(collection.find({'address': address}))
        
        elif collection.count_documents({'rif_supplier': rif}, limit = 1):
            return 'ya existe un RIF así'
        
        elif collection.count_documents({'phone_supplier': phone}, limit = 1):
            return 'ya existe un teléfono así'
        
        else:

            post = {'name_supplier': name, 'address_supplier': address, 'rif_supplier': rif, 'phone_supplier': phone, 'state_supplier': 1}
            collection.insert_one(post)

            return True
        
    def UpdateSupplier(nameSupplier, addressSupplier, rifSupplier, phoneSupplier, idObject):
        
        query = {}
        collection = DataBase.db['supplier']

        #Revisa si el dato existe en otros proveedores
        if collection.count_documents( {
                "_id":  {"$nin" : [ObjectId(idObject)]},
                "name_supplier": nameSupplier,
                "state_supplier": 1
            }):
            return ', ya existe registrado este nombre.'
        elif collection.count_documents( {
                "_id":  {"$nin" : [ObjectId(idObject)]},
                'address_supplier': addressSupplier,
                "state_supplier": 1
            }):
            return ', ya existe registrado esta dirección.'
        elif collection.count_documents( {
                "_id":  {"$nin" : [ObjectId(idObject)]},
                'rif_supplier': rifSupplier,
                "state_supplier": 1
            }):
            return ', ya existe registrado este RIF.'
        elif collection.count_documents( {
                "_id":  {"$nin" : [ObjectId(idObject)]},
                'phone_supplier': phoneSupplier,
                "state_supplier": 1
            }):
            return ', ya existe registrado este número de teléfono.'

        else:
            #data
            ####Si no es el mismo el dato introducido anteriormente, lo añade al query
            #name_supplier
            if collection.count_documents({'_id': ObjectId(idObject), 'name_supplier': nameSupplier}, limit = 1) <= 0:
                query['name_supplier'] = nameSupplier

            #address_supplier
            if collection.count_documents({'_id': ObjectId(idObject), 'address_supplier': addressSupplier}, limit = 1) <= 0:
                query['address_supplier'] = addressSupplier

            #rif_supplier
            if collection.count_documents({'_id': ObjectId(idObject), 'rif_supplier': rifSupplier}, limit = 1) <= 0:
                query['rif_supplier'] = rifSupplier

            #phone_supplier
            if collection.count_documents({'_id': ObjectId(idObject), 'phone_supplier': phoneSupplier}, limit = 1) <= 0:
                query['phone_supplier'] = phoneSupplier

            #Si no tiene items el query (no hay datos nuevos), regresar si hacer cambios  a la base de datos
            if len(query) == 0:
                return ', los datos ingresados son los mismos que habia antes.'
            else:
                collection.update_one({'_id': ObjectId(idObject)},{'$set': query })
                return True
    
    def DeleteSupplier(id):

        collection = DataBase.db['supplier']
        collection_products = DataBase.db['products']
        collection_charges = DataBase.db['charges']


        #results_charges = collection_charges.find_one({'id_supplier': id}, {'_id': 1, 'products.amount_product': 1}, sort=({'date': -1}))

        results_charges = collection_charges.aggregate([
            { '$match': { 'id_supplier': id } },
            { '$limit': 1},
            { '$project' : 
                { '_id':0, 'products.id_product' : 1 , 'products.amount_product' : 1 } 
            }
        
        ])

        list_results_charges = list(results_charges)

        if len(list_results_charges) > 0:

            for item in list_results_charges[0]['products']:
                
                result_product = collection_products.find_one({'_id': item['id_product']})

                
                if result_product:

                    amount_actual = int(result_product['amount_product']) - int(item['amount_product']) 

                    print('AMOUNT')
                    print(amount_actual)
                    print(item['id_product'])
                    print()

                    if amount_actual > 0:

                        query = {'amount_product': str(amount_actual)}

                        collection_products.update_one({'_id': item['id_product']},{'$set': query })
                    else:
                        
                        query = {'state_product': 2}

                        collection_products.update_one({'_id': item['id_product']},{'$set': query })
                
        query = {'state_supplier': 0}

        collection.update_one({'_id': id},{'$set': query })
        

    def SearchSupplier(id):
        collection = DataBase.db['supplier']

        result = collection.find_one({'_id': ObjectId(id)})
        
        return result