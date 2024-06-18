import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId

last_id = previous_id = None

name_collection = 'clients'
API = DataBase.DatabaseClass
class ClientsDB():



    def ShowData(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        #collection = DataBase.db['clients']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        #starting_id = collection.find({'state_client': 1})

        starting_id = API.Find(
            name_collection,
            {'state_client': 1},
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

            results = API.Find(
                name_collection, 
                {'state_client': 1},
                {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1},
                start, 
                end, 
                {'_id': 1}
            )
            #results = collection.find({'state_client': 1}, {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1}).skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})
            
            #cantidad de productos que se encontraron
            amount_items = API.CountDocument(
                name_collection,
                {'state_client': 1},
                start,
                end
            )
            #amount_items = collection.count_documents({'state_client': 1}, skip=start, limit=end)

            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':

                results = API.Find(
                    name_collection, 
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_client': 1},
                    {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1},
                    None, 
                    end, 
                    None
                )

                #results = collection.find({'_id': {'$gt': last_id}, 'state_client': 1}, {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                #results1 = collection.find({'_id': {'$gt': last_id}}).limit( end )#.sort({ '_id' : ObjectId(last_id)})
                amount_items = API.CountDocument(
                    name_collection,
                    {'_id': {'$gt': { "$oid": last_id}}, 'state_client': 1},
                    None,
                    end
                )
                #amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_client': 1}, limit=end)


                #last_item = len(list(results1)) - 1
                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':
                #results = collection.find({'_id': {'$gte': previous_id}, 'state_client': 1}, {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})
                
                results = API.Find(
                    name_collection, 
                    {'_id': {'$gte': { "$oid": previous_id}}, 'state_client': 1},
                    {'_id': 1, 'name_client': 1, 'id_client': 1, 'phone_client': 1},
                    None, 
                    end, 
                    None
                )

                #amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_client': 1}, limit=end)
                
                amount_items = API.CountDocument(
                    name_collection,
                    {'_id': {'$gte': {"$oid": previous_id }}, 'state_client': 1},
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
        numbers_collection = API.CountDocument(
                    name_collection,
                    {'state_client': 1},
                    None,
                    None
                )
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

        if API.CountDocument(
            name_collection,
            {
                'name_client': name,
            },
            None,
            None
        ):
            return 'ya existe un nombre así.'
        
        #if collection.count_documents({'name_client': name}, limit = 1):

        #    return 'ya existe un nombre así.'
        elif API.CountDocument(
            name_collection,
            {
                'id_client': id,
            },
            None,
            None
        ):
            return 'ya existe una cédula así registrada.'   
        #elif collection.count_documents({'id_client': id}, limit = 1):
            #return 'ya existe una cédula así registrada.'

        elif API.CountDocument(
            name_collection,
            {
                'phone_client': phone,
            },
            None,
            None
        ):
            return 'ya existe un teléfono así.'   
        #elif collection.count_documents({'phone_client': phone}, limit = 1):
        #    return 'ya existe un teléfono así.'
        
        else:

            #data
            document = {'name_client': name, 'id_client': id, 'phone_client': phone, 'state_client': 1}
            #collection.insert_one(post)

            API.InsertInto(
                name_collection, 
                document
            )
            
            return True
    
    def UpdateClient(nameClient, idClient, phoneClient, idObject):
        
        query = {}
        #collection = DataBase.db['clients']

        #Revisa si el dato existe en otros proveedores
        if API.CountDocument(
                name_collection,
                {
                    "_id": {"$nin" : [{ "$oid": idObject }]},
                    'name_client': nameClient,
                    "state_client": 1
                },
                None,
                None
            ):
            return ', ya existe registrado este nombre.'

        #if collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        'name_client': nameClient,
        #        "state_client": 1
        #    }):
            #return ', ya existe registrado este nombre.'

        elif API.CountDocument(
                name_collection,
                {
                    "_id": {"$nin" : [{ "$oid": idObject }]},
                    'id_client': idClient,
                    "state_client": 1
                },
                None,
                None
            ):
            return ', ya existe registrado esta cédula.'
        #elif collection.count_documents( {
        #        "_id":  {"$nin" : [ObjectId(idObject)]},
        #        'id_client': idClient,
        #        "state_client": 1
        #    }):
        #    return ', ya existe registrado esta cédula.'
        elif API.CountDocument(
                name_collection,
                {
                    "_id": {"$nin" : [{ "$oid": idObject }]},
                    'phone_client': phoneClient,
                    "state_client": 1
                },
                None,
                None
            ):
            return ', ya existe registrado este número de teléfono.'

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
            if API.CountDocument(
                name_collection,
                {
                    "_id": {"$nin" : [{ "$oid": idObject }]},
                    'name_client': nameClient,
                },
                None,
                None
            ) == None:
                query['name_client'] = nameClient

            #if collection.count_documents({'_id': ObjectId(idObject), 'name_client': nameClient}, limit = 1) <= 0:
            #    query['name_client'] = nameClient

            #id_client
            if API.CountDocument(
                name_collection,
                {
                    "_id": {"$nin" : [{ "$oid": idObject }]},
                    'id_client': idClient,
                },
                None,
                None
            ) == None:
                query['id_client'] = idClient
                
            #if collection.count_documents({'_id': ObjectId(idObject), 'id_client': idClient}, limit = 1) <= 0:
            #    query['id_client'] = idClient

            #phone_client
            if API.CountDocument(
                name_collection,
                {
                    "_id": {"$nin" : [{ "$oid": idObject }]},
                    'phone_client': phoneClient,
                },
                None,
                None
            ) == None:
                query['phone_client'] = phoneClient
                
            #if collection.count_documents({'_id': ObjectId(idObject), 'phone_client': phoneClient}, limit = 1) <= 0:
            #    query['phone_client'] = phoneClient

            #Si no tiene items el query (no hay datos nuevos), regresar si hacer cambios  a la base de datos
            if len(query) == 0:
                return True
            else:
                #collection.update_one({'_id': ObjectId(idObject)},{'$set': query })
                
                result = API.UpdateOne(
                    name_collection,
                    {'_id': {'$oid': idObject}},
                    query
                )

                return result

    def DeleteClient(id):

        #collection = DataBase.db['clients']
        query = {'state_client': 0}

        result = API.UpdateOne(
                    name_collection,
                    {'_id': {'$oid': id}},
                    query
                )
        
        return result

        #collection.update_one({'_id': id},{'$set': query })

    def SearchUser(id):
        #collection = DataBase.db['clients']

        #result = collection.find_one({'_id': ObjectId(id)})
        
        result = API.FindOne(
            name_collection,
            {"_id": { "$oid": id }},
            None
        )
        return result