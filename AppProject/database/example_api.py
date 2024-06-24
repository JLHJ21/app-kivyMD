#FIND
a = {
    #nombre de la coleccion
    "collection_choose": "supplier", 
    #archivo a buscar
    "search_query": 
        {
            "name_supplier": "cambio de nombre"
        },
    #dato a mostrar
    "projection": {
        "name_supplier": 1,
        "_id": 1
    },
    #cantidad de archivos a saltar
    "skip":0,
    #cantidad de resultados
    "limit": 2,
    #como se ordenarán
    "sort": {
        "_id":-1
    }
}

#FIND_ONE
a = {
    #nombre de la coleccion
    "collection_choose": "supplier", 
    #archivo a buscar
    "search_query": 
        {
            "name_supplier": "cambio de nombre"
        },
    #dato a mostrar
    "projection": {
        "name_supplier": 1,
        "_id": 1
    },
}

#UPDATE_ONE
a = {
    #nombre de la coleccion
    "collection_choose": "supplier", 
    #archivo a buscar
    "search_query": 
        {
            "_id": "ObjectId('66761136a8d5d14625849ed8')"
        },
    #dato a cambiar
    "update_query":
        {"$set":
            {
                "name_supplier": "cambio de nombre"
            },
        }
}

#INSERT INTO
a = {
    #nombre de la colección
    "collection_choose": "sales", 
    #datos a agregar en la coleccion
    "document_insert":
            {
                "name_supplier": "ObjectId('666cec0f8eab02d521894849')",
                "address_supplier": "addressprueba12",
                "rif_supplier": "rifprueba12",
                "phone_supplier": "phoneprueba12",
                "state_supplier": 1
            },
            
    
    }

#COUNT_DOCUMENT
a = {
    #nombre de la coleccion
    "collection_choose": "supplier", 
    #archivo a buscar
    "search_query": 
        {
            "_id": "ObjectId('66761136a8d5d14625849ed8')"
        },
    
    "skip": "None",
    "limit": "None"
}

#AGGREGATE PARA OBTENER DATOS DE ARRAYS
a = {
    #nombre de la coleccion
    "collection_choose": "charges", 
    #archivo a buscar
    "search_query": 
        {
            "id_supplier": "ObjectId('665bd24669ed9acabb259fea')"
        },
    #cantidad de resultados
    "limit": "None",
    #aggregate a realizar, puede ser para obtener datos de arrays como contarlos
        "projection": { '_id': 0, 'products_sales.id_product' : 1 , 'products_sales.amount_wanted' : 1 }
}

#AGGREGATE PARA OBTENER LA ***CANTIDAD*** DEL ARRAY
a = {
    #nombre de la coleccion
    "collection_choose": "sales", 
    #archivo a buscar
    "search_query": 
        {
            "_id": "ObjectId('666c2af993bb21c21f3e97e2')"
        },
    #cantidad de resultados
    "limit": "None",
    #aggregate a realizar, puede ser para obtener datos de arrays como contarlos
    "projection": { '_id' : 0 , 'productsAmount': { '$size': "$products_sales" } }
}



starting_id = functions.FunctionsKivys.GetResultFromDatabase(query, 'find')

