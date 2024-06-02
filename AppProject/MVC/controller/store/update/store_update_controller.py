from kivymd.uix.screen import MDScreen

from kivy.properties import BooleanProperty, ObjectProperty, ListProperty, StringProperty, NumericProperty 
from kivy.metrics import dp

from MVC.model.store.store_model import StoreDB
from MVC.model.charges.charges_model import ChargesDB

import MVC.controller.functions as functions

import concurrent.futures

#Pagina de almacen modificar
class StoreUpdatePage(MDScreen):

    
    idObject= StringProperty('')
    RV= ObjectProperty('')

    nameProduct = StringProperty('')
    amountProduct= StringProperty('')
    profitProduct = StringProperty('')
    supplierProduct = StringProperty('')
    

    def on_pre_enter(self):

        from templates.table.table import global_id_modal, global_modal_rv

        self.idObject = str(global_id_modal)
        self.RV = global_modal_rv

        dataClient = StoreDB.SearchProduct(self.idObject)

        self.nameProduct = dataClient['name_product']
        self.amountProduct= dataClient['amount_product']
        self.profitProduct = dataClient['profit_product']
        self.supplierProduct = dataClient['name_supplier']

    def UpdateProduct(self, nameProduct, amountProduct, profitProduct, supplierProduct):
        
        #print(name, id, phone)
        results = StoreDB.UpdateProduct(nameProduct, amountProduct, profitProduct, supplierProduct, self.idObject)
        
        if results == True:
            functions.FunctionsKivys.ChangePage('StorePage', 'Almacen')


    ##SELECCIONAR PROVEEDOR

    #MENU DE PROVEEDORES
    def SelectItem(self, nameSupplier, nameID):
        
        self.ids.searchingSupplier.text = nameSupplier
        self.ids.searchingSupplier.name = nameID
        self.ids.searchingSupplier.icon_left = "account-check"

        #self.ids.searchingSupplier.icon_left = 'account-star'

        #Cambiar altura del RecycleView
        self.ids.gridLayoutrvV.height = dp(0)
        self.ids.rvV.data = []

    def list_suppliers(self, text=""):

        #Cambiar altura del RecycleView
        self.ids.gridLayoutrvV.height = dp(100)
        self.ids.searchingSupplier.icon_left = ""

        def add_icon_item(text, name, zero_items):

            if zero_items == True:
                icon = "account-eye"
                callback = lambda x='a': self.SelectItem(text, name)

            elif zero_items == False:
                icon = "account-cancel"
                callback = lambda x='a': x

            #print(App.get_running_app().get_screen('ChargeAddPage'))#.root.get_screen('ChargeAddPage').ids.rv.data )
            
            self.ids.rvV.data.append(
                    {
                        "viewclass": "CustomOneLineIconListItem",
                        "icon": icon,
                        "text": text,
                        "name": name,
                        "on_release": callback
                    }
                )

        self.ids.rvV.data = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(ChargesDB.GetDataSupplier, text)
            return_value = future.result()


        if (len(return_value)) <= 0:
            
            text = 'No hay algún proveedor registrado con el nombre que escribiste.'
            name = 'None'
            add_icon_item(text, name, False)
        else:

            for item in return_value:

                text = return_value[item]['name_supplier']
                name = return_value[item]['_id']

                add_icon_item(text, name, True)