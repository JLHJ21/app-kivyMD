from kivymd.uix.screen import MDScreen
from MVC.model.supplier.supplier_model import SupplierDB
import MVC.controller.functions as functions

class SupplierAddPage(MDScreen):


    def AddNewSupplier(self, name, address, rif, phone):
        
        #print(name, address, rif, phone)
        results = SupplierDB.CreateSupplier(name, address, rif, phone)
        
        if results == True:
            functions.FunctionsKivys.ChangePage('SupplierPage', 'Proveedor')


        pass

    pass