from kivymd.uix.screen import MDScreen
from MVC.model.supplier.supplier_model import SupplierDB

import MVC.controller.functions as functions
import concurrent.futures

self_supplier_page = None
#PAGINA DE PROVEEDOR
class SupplierPage(MDScreen):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_supplier_page
        self_supplier_page = self

    
    def ChangePageSupplierPage(self):

        functions.FunctionsKivys.ChangePage('self', 'SupplierAddPage', 'Proveedor - Agregar')
        

    def ShowDataSupplierController(self, start, end, state):

        '''
        async_result = pool.apply_async(SupplierDB.ShowData, (start, end)) # tuple of args for foo
        # do some other stuff in the main process
        return_val = async_result.get()  # get the return value from your function. 
        return return_val

        '''

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(SupplierDB.ShowData, start,end,state)
            return_value = future.result()

            return return_value
        

    def CallbackMenuSupplier(self, button):

        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuTypeSupplierPage)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeSupplier(self = None, Text = ""):

        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_supplier_page, functions.global_variable_self.MenuTypeSupplierPage, 'ButtonMenuSearchingSupplier', Text)
