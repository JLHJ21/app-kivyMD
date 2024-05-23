import database.database as DataBase
from pymongo import ASCENDING
from bson import ObjectId

last_id = previous_id = None

class ClientsDB():



    def ShowData(start, end, state = ''):

        #PERMITE QUE PERSISTA EL PRIMER Y ULTIMO ID, 
        global last_id, previous_id

        #CONEXION A LA COLECCION
        collection = DataBase.db['clients']

        #OBTIENE TODOS LOS DATOS DE LA COLECCION
        starting_id = collection.find()

        #SI EL ESTADO ES NONE, REINICIA LAS VARIABLES GLOBALES
        if state == '':
            last_id = previous_id = None

        #SE ACTIVA AL SER LA PRIMERA LLAMADA A LA BASE DE DATOS
        if last_id == None:

            #OBTIENE LOS DATOS DE LA COLECCION
            results = collection.find().skip(start).limit( end ).sort({'_id': 1}) #.sort({ '_id' : -1})
            last_id = results[end - 1]['_id']

        else:

            #SI SE DA CLICK AL BOTON DE SIGUIENTE
            if state == 'next':
                results = collection.find({'_id': {'$gt': last_id}}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                results1 = collection.find({'_id': {'$gt': last_id}}).limit( end )#.sort({ '_id' : ObjectId(last_id)})

                last_item = len(list(results1)) - 1
                last_id = results[last_item]['_id']

                
                if (start - end) - 1 < 0:
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - end) - 1]['_id']

            #SI SE DA CLICK AL BOTON DE ATRÁS
            elif state == 'previous':
                results = collection.find({'_id': {'$gte': previous_id}}).limit( end )#.sort({ '_id' : ObjectId(last_id)})
                
                #OBTIENE EL ULTIMO ID DEL ITEM DE LA COLECCION
                last_id = results[end - 1]['_id']

                if (start - end) - 1 < 0:
            
                    previous_id = starting_id[0]['_id']
                    
                else:
                    previous_id = starting_id[(start - end) - 1]['_id']

        #SE CREA DICCIONARIO QUE ALMACENARÁ LOS DATOS OBTENIDOS DE LA BASE DE DATOS
        list_results = {}
        #CUANTA LA CANTIDAD DE DOCUMENTOS DE LA COLECCIÓN
        numbers_collection = collection.count_documents({})#, skip=start, limit=end)

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
            
        collection = DataBase.db['clients']

        #data

        post = {'name': name, 'id': id, 'phone': phone}
        collection.insert_one(post)

        return True