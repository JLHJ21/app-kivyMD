import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId

last_id = previous_id = None

class StoreDB():

    def ShowDataStoreModel(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        collection = DataBase.db['products']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        starting_id = collection.find({'state_product': 1})

        #SI EL ESTADO ES NONE, REINICIA LAS VARIABLES GLOBALES
        if state == '':
            last_id = previous_id = None

        #SE ACTIVA AL SER LA PRIMERA LLAMADA A LA BASE DE DATOS
        if last_id == None:

            #OBTIENE LOS DATOS DE LA COLECCION
            results = collection.find({'state_product': 1}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1}).skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})
            
            #cantidad de productos que se encontraron
            amount_items = collection.count_documents({'state_product': 1}, skip=start, limit=end)

            #Obtiene el ultimo id del producto
            last_id = results[amount_items - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':

                results = collection.find({'_id': {'$gt': last_id}, 'state_product': 1}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1} ).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                amount_items = collection.count_documents({'_id': {'$gt': last_id}, 'state_product': 1}, limit=end)
                last_id = results[amount_items - 1]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':
                results = collection.find({'_id': {'$gte': previous_id}, 'state_product': 1}, {'_id': 1, 'name_product': 1, 'amount_product': 1, 'profit_product': 1, 'name_supplier': 1}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                amount_items = collection.count_documents({'_id': {'$gte': previous_id}, 'state_product': 1}, limit=end)
                
                #OBTIENE EL ULTIMO ID DEL ITEM DE LA COLECCION
                last_id = results[amount_items - 1]['_id']

                if (start - end) - 1 < 0:
            
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - amount_items) - 1]['_id']

        #SE CREA DICCIONARIO QUE ALMACENARÁ LOS DATOS OBTENIDOS DE LA BASE DE DATOS
        list_results = {}
        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        numbers_collection = collection.count_documents({'state_product': 1})#, skip=start, limit=end)

        #SE AGREGA SIEMPRE COMO PRIMER DATO, LAS CARACTERISTICAS (CANTIDAD DE DOCUMENTOS, ARCHIVO COMIENZA, ARCHIVO TERMINADA)
        list_results.update({'characteristics': [numbers_collection, start, end]})

        
        #CICLO FOR QUE AGREGA LOS DATOS OBTENIDO DE LA BASE DE DATOS AL DICCIONARIO LIST_RESULTS, ESTO HACE QUE LA VARIABLE RESULTS(CURSOR) SE VACIE 
        for index, i in enumerate(results):

            #LO ALMACENA DE FORMA, DATO(POSICION): 'TODA LA INFORMACIÓN DE LA BASE DE DATOS
            d = {f"dato{index}": [(i)]}

            list_results.update(d)

        #RETORNA LA INFORMACIÓN OBTENIDO

        return list_results

    '''
    def CreateSupplier(name, address, rif, phone):
            
        collection = DataBase.db['supplier']

        #data

        if collection.count_documents({'name': name}, limit = 1):

            return 'name: ' + str(collection.find({'name': name}))

        #elif collection.count_documents({'address': address}, limit = 1):
        #    return 'address: ' + str(collection.find({'address': address}))
        
        elif collection.count_documents({'rif': rif}, limit = 1):
            return 'rif: ' + str(collection.find({'rif': rif}))
        
        elif collection.count_documents({'phone': phone}, limit = 1):
            return 'phone: ' + str(collection.find({'phone': phone}))
        
        else:


            post = {'name': name, 'address': address, 'rif': rif, 'phone': phone}
            collection.insert_one(post)

            return True
    '''
    #def UpdateProduct(nameProduct, amountProduct, profitProduct, supplierProduct, idObject):
    def UpdateProduct(nameProduct, profitProduct, supplierProduct, idObject):
        
        query = {}
        collection = DataBase.db['products']

        
        #Revisa si el dato existe en otros proveedores
        if collection.count_documents( {
                "_id":  {"$nin" : [ObjectId(idObject)]},
                'name_product': nameProduct,
                "state_product": 1
            }):
            return ', ya existe registrado este nombre.'

        else:
            #data
            ####Si no existe el dato introducido, lo añade al query
            #name_product
            if collection.count_documents({'_id': ObjectId(idObject), 'name_product': nameProduct}, limit = 1) <= 0:
                query['name_product'] = nameProduct

            #amount_product
            #if collection.count_documents({'_id': ObjectId(idObject), 'amount_product': amountProduct}, limit = 1) <= 0:
            #    query['amount_product'] = amountProduct

            #profit_product
            if collection.count_documents({'_id': ObjectId(idObject), 'profit_product': profitProduct}, limit = 1) <= 0:
                query['profit_product'] = profitProduct

            #name_supplier
            if collection.count_documents({'_id': ObjectId(idObject), 'name_supplier': supplierProduct}, limit = 1) <= 0:
                query['name_supplier'] = supplierProduct

            ##########
            #Si no tiene items el query (no hay datos nuevos), regresar si hacer cambios  a la base de datos
            if len(query) == 0:
                return ', los datos ingresados son los mismos que habia antes.'
            else:
                collection.update_one({'_id': ObjectId(idObject)},{'$set': query })
                return True

    
    def DeleteProduct(id):

        collection = DataBase.db['products']

        query = {'state_product': 0}

        collection.update_one({'_id': id},{'$set': query })

    def SearchProduct(id):
        collection = DataBase.db['products']

        result = collection.find_one({'_id': ObjectId(id)})
        
        return result