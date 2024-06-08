from kivymd.uix.screen import MDScreen
from kivymd.toast import toast

import concurrent.futures

from MVC.model.supplier.supplier_model import SupplierDB
import MVC.controller.functions as functions

class SupplierAddPage(MDScreen):
    
    def AddNewSupplier(self, name, address, rif, phone):
        
        #print(name, address, rif, phone)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(SupplierDB.CreateSupplier, name, address, rif, phone)
            results = future.result()
        
        if results == True:
            
            from MVC.controller.supplier.supplier_controller import self_supplier_page
            from templates.table.table import ModalsDialog

            objecto = self_supplier_page.ids.tableSuppliers.objecto
            objectoRv = self_supplier_page.ids.tableSuppliers.objecto.rv

            #el primero es el objecto (variable objecto que lleva el widget weak), el segundo es el objecto.rv del recycleview
            ModalsDialog.ActualizeData(objecto, objectoRv)
            toast('¡Proveedor agregado con éxito!')            
            functions.FunctionsKivys.ChangePage('self', 'SupplierPage', 'Proveedor')
        else:
            toast('Hubo un error, ' + str(results))
