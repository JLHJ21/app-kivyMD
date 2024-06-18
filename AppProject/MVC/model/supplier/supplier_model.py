import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId

last_id = previous_id = None

name_collection = 'supplier'
API = DataBase.DatabaseClass
class SupplierDB():



    def ShowData(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        #collection = DataBase.db['supplier']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        #starting_id = collection.find({'state_supplier': 1})

        starting_id = API.Find(
            name_collection,
            {'state_supplier': 1},
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
            #results = collection.find({'state_supplier': 1}, {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1}).skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})
            results = API.Find(
                name_collection, 
                {'state_supplier': 1},
                {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1},
                start, 
                end, 
                {'_id': 1}
            )
            #cantidad de productos que se encontraron
            #amount_items = collection.count_documents({'state_supplier': 1}, skip=start, limit=end)
            amount_items = API.CountDocument(
                name_collection,
                {'state_supplier': 1},
                start,
                end
            )
            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':

                results = API.Find(
                    name_collection, 
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_supplier': 1},
                    {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1},
                    None, 
                    end, 
                    None
                )

                #results = collection.find({'_id': {'$gt': last_id}, 'state_supplier': 1}, {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                amount_items = API.CountDocument(
                    name_collection,
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_supplier': 1},
                    None,
                    end
                )
                #amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_supplier': 1}, limit=end)
                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':

                results = API.Find(
                    name_collection, 
                    {'_id': {'$gte': { "$oid": previous_id}}, 'state_supplier': 1},
                    {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1},
                    None, 
                    end, 
                    None
                )
                #results = collection.find({'_id': {'$gte': previous_id}, 'state_supplier': 1}, {'_id': 1, 'name_supplier': 1, 'address_supplier': 1, 'rif_supplier': 1, 'phone_supplier': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                #amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_supplier': 1}, limit=end)
                amount_items = API.CountDocument(
                    name_collection,
                    {'_id': {'$gte': {"$oid": previous_id }}, 'state_supplier': 1},
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
        #numbers_collection = collection.count_documents({'state_supplier': 1})#, skip=start, limit=end)
        numbers_collection = API.CountDocument(
                    name_collection,
                    {'state_supplier': 1},
                    None,
                    None
                )
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
        if API.CountDocument(
            name_collection,
            {
                'name_supplier': name,
            },
            None,
            None
        ):
            return 'ya existe un nombre así'
        #if collection.count_documents({'name_supplier': name}, limit = 1):
        #    return 'ya existe un nombre así'

        #elif collection.count_documents({'address': address}, limit = 1):
        #    return 'address: ' + str(collection.find({'address': address}))
        

        elif API.CountDocument(
            name_collection,
            {
                'rif_supplier': rif,
            },
            None,
            None
        ):
            return 'ya existe un RIF así'

        #elif collection.count_documents({'rif_supplier': rif}, limit = 1):
        #    return 'ya existe un RIF así'
        
        elif API.CountDocument(
            name_collection,
            {
                'phone_supplier': phone,
            },
            None,
            None
        ):
            return 'ya existe un teléfono así'

        #elif collection.count_documents({'phone_supplier': phone}, limit = 1):
        #    return 'ya existe un teléfono así'
        
        else:

            document = {'name_supplier': name, 'address_supplier': address, 'rif_supplier': rif, 'phone_supplier': phone, 'state_supplier': 1}
            #collection.insert_one(post)

            API.InsertInto(
                name_collection, 
                document
            )

            return True
        
    def UpdateSupplier(nameSupplier, addressSupplier, rifSupplier, phoneSupplier, idObject):
        
        query = {}
        #collection = DataBase.db['supplier']

        #Revisa si el dato existe en otros proveedores
        if API.CountDocument(
                name_collection,
                {
                    "_id": {"$nin" : [{ "$oid": idObject }]},
                    "name_supplier": nameSupplier,
                    "state_supplier": 1
                },
                None,
                None
            ):
            return ', ya existe registrado este nombre.'
        #if collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        "name_supplier": nameSupplier,
        #        "state_supplier": 1
        #    }):
        #    return ', ya existe registrado este nombre.'
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
        #elif collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        'address_supplier': addressSupplier,
        #        "state_supplier": 1
        #    }):
        #    return ', ya existe registrado esta dirección.'
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
        
        #elif collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        'rif_supplier': rifSupplier,
        #        "state_supplier": 1
        #    }):
        #    return ', ya existe registrado este RIF.'

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

            #address_supplier
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
            #if collection.count_documents({'_id': ObjectId(idObject), 'address_supplier': addressSupplier}, limit = 1) <= 0:
            #    query['address_supplier'] = addressSupplier

            #rif_supplier
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
            #if collection.count_documents({'_id': ObjectId(idObject), 'rif_supplier': rifSupplier}, limit = 1) <= 0:
            #    query['rif_supplier'] = rifSupplier

            #phone_supplier
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
            #if collection.count_documents({'_id': ObjectId(idObject), 'phone_supplier': phoneSupplier}, limit = 1) <= 0:
            #    query['phone_supplier'] = phoneSupplier

            #Si no tiene items el query (no hay datos nuevos), regresar si hacer cambios  a la base de datos
            if len(query) == 0:
                return ', los datos ingresados son los mismos que habia antes.'
            else:

                result = API.UpdateOne(
                    name_collection,
                    {'_id': {'$oid': idObject}},
                    query
                )

                return result
                #collection.update_one({'_id': ObjectId(idObject)},{'$set': query })
                #return True
    
    def DeleteSupplier(id):

        #collection = DataBase.db['supplier']
        #collection_products = DataBase.db['products']
        #collection_charges = DataBase.db['charges']
        
        results_charges = API.Aggregate(
            'charges',
            { 'id_supplier': {'$oid': id} },
            None,
            1,
            { '_id': 1, 'products.id_product' : 1 , 'products.amount_product' : 1 } 
        )

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

                result_product = API.FindOne(
                    'products',
                    {'_id': {'$oid': item['id_product']}},
                    None
                )

                
                if result_product:

                    amount_actual = int(result_product['amount_product']) - int(item['amount_product']) 

                    if amount_actual > 0:

                        query = {'amount_product': str(amount_actual)}

                        API.UpdateOne(
                            'products',
                            { '_id': {'$oid': item['id_product']} },
                            query
                        )

                        #collection_products.update_one({'_id': item['id_product']},{'$set': query })
                    else:
                        
                        query = {'state_product': 2}

                        #collection_products.update_one({'_id': item['id_product']},{'$set': query })

                        API.UpdateOne(
                            'products',
                            { '_id': {'$oid': item['id_product']} },
                            query
                        )
                
        query = {'state_supplier': 0}

        API.UpdateOne(
            name_collection,
            { '_id': {'$oid': id} },
            query
        )

        #collection.update_one({'_id': id},{'$set': query })
        

    def SearchSupplier(id):
        #collection = DataBase.db['supplier']

        #result = collection.find_one({'_id': ObjectId(id)})
        
        result = API.FindOne(
            name_collection,
            {"_id": { "$oid": id }},
            None
        )
        return result
        #return result