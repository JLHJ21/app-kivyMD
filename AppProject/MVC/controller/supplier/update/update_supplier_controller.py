from kivymd.uix.screen import MDScreen

from kivy.properties import BooleanProperty, ObjectProperty, ListProperty, StringProperty, NumericProperty 

from MVC.model.supplier.supplier_model import SupplierDB
import MVC.controller.functions as functions

class SupplierUpdatePage(MDScreen):

    
    idObject = StringProperty('')
    RV = ObjectProperty('')

    nameSupplier = StringProperty('')
    addressSupplier = StringProperty('')
    rifSupplier = StringProperty('')
    phoneSupplier = StringProperty('')

    def on_pre_enter(self):

        from templates.table.table import global_id_modal, global_modal_rv

        self.idObject = str(global_id_modal)
        self.RV = global_modal_rv

        dataSupplier = SupplierDB.SearchSupplier(self.idObject)

        self.nameSupplier = dataSupplier['name_supplier']
        self.addressSupplier = dataSupplier['address_supplier']
        self.rifSupplier = dataSupplier['rif_supplier']
        self.phoneSupplier = dataSupplier['phone_supplier']


    def UpdateSupplier(self, nameSupplier, addressSupplier, rifSupplier, phoneSupplier):
        
        #print(name, id, phone)
        results = SupplierDB.UpdateSupplier(nameSupplier, addressSupplier, rifSupplier, phoneSupplier, self.idObject)
        
        if results == True:
            functions.FunctionsKivys.ChangePage('SupplierPage', 'Proveedor')
