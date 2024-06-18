import database.database as DataBase
import MVC.controller.functions as functions
from datetime import datetime


name_collection = 'foreign_exchange'
API = DataBase.DatabaseClass
class ForeignExchangeDB():

    def GetForeignExchange():
        
        #collection = DataBase.db['foreign_exchange']
        #results = collection.find_one()

        results = API.FindOne(
            name_collection,
            None,
            None,
        )
        
        return results
    
    def UpdateRateMoney(dolar, bolivar):
        query = {}

        #SI LOS DATOS NO SE REPITEN, SE AGREGA AL QUERY PARA MODIFICAR DATO
        if (bolivar == functions.rate_bolivar) == False:
            #OJO
            #functions.rate_bolivar = bolivar
            query['rate_bolivar'] = bolivar
            
        #SI LOS DATOS NO SE REPITEN, SE AGREGA AL QUERY PARA MODIFICAR DATO
        if (dolar == functions.rate_dolar) == False:
            #OJO
            #functions.rate_dolar = dolar
            query['rate_dolar'] = dolar

        if len(query) == 0:
            return ', no hay ningun dato por cambiar.'
        else:

            #collection = DataBase.db['foreign_exchange']

            last_change = datetime.today().strftime('%d-%m-%Y')
            query['last_change'] = last_change

            #documentToChange = {'money_preference': functions.money_preference}
            #newValue = { "$set":  query  }


            result = API.UpdateOne(
                name_collection,
                {'_id': {'$oid': '6668ef8bc265ac0f72985b42'}},
                query
            )

            #collection.update_one(documentToChange, newValue)

            return result
        
    def UpdateMoneyPreference(new_preference):
        try:
            #collection = DataBase.db['foreign_exchange']

            last_change = datetime.today().strftime('%d-%m-%Y')
            documentToChange = {'money_preference': functions.money_preference}
            query = { 'money_preference': new_preference, 'last_change': last_change }
            
            #newValue = { "$set": { 'money_preference': new_preference, 'last_change': last_change } }

            #collection.update_one(documentToChange, newValue)
            result = API.UpdateOne(
                name_collection,
                documentToChange,
                query
            )

            functions.money_preference = new_preference

            return result
        except:
            return ', error al usar la base de datos.'
        

    '''
    def ChangePreferenceExchangeForeign(preference = None):

        collection = DataBase.db['foreign_exchange']
        dataList = []

        if preference == None:
            pass
        else:
            #FALSO LA PREFERENCIA
            documentToChange = { 'preference': True}
            newValue = { "$set": { "preference": False } }

            collection.update_one(documentToChange, newValue)


            #TRUE LA PREFERENCIA
            documentToChange = { "name": preference }
            newValue = { "$set": { "preference": True } }

            collection.update_one(documentToChange, newValue)

        results = collection.find_one({'preference': True})

        #Valores
        dolar = results['changeToDolar']
        peso = results['changeToPeso']
        bolivar = results['changeToBolivar']
        nombre = results['name']


        dataList.extend([dolar, peso, bolivar, nombre])

        return dataList
    

    def UpdateForeignExchangeData(dolar, peso, bolivar):
        #DOLAR
        if len(dolar) < 1:

            #DOLAR
            documentToChange = { "name": 'dolar' }
            newValue = { "$set": { "changeToPeso": peso, "changeToBolivar": bolivar } }

        #PESO
        elif len(peso) < 1:
            #PESO
            documentToChange = { "name": 'peso' }
            newValue = { "$set": { "changeToDolar": dolar, "changeToBolivar": bolivar } }

        #BOLIVAR
        elif len(bolivar) < 1:
            #BOLIVAR
            documentToChange = { "name": 'bolivar' }
            newValue = { "$set": { "changeToDolar": dolar, "changeToPeso": peso } }


        collection = DataBase.db['foreign_exchange']
        collection.update_one(documentToChange, newValue)
      

    def ShowDataExchangeForeign(name):
        collection = DataBase.db['foreign_exchange']
        dataList = []
        

        results = collection.find_one({'preference': True})

        dataList.append(results['changeToDolar'])

        return dataList
    
    '''
