import database.database as DataBase


class ForeignExchangeDB():

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
