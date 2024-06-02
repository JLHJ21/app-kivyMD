
from kivymd.uix.screen import MDScreen
from MVC.model.store.store_model import StoreDB
#from MVC.controller.functions import MenuAndTitleSelect, global_variable_self

import MVC.controller.functions as functions
import concurrent.futures

#PAGINA DE ALMACEN
class StorePage(MDScreen):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_store_page
        self_store_page = self

    def CallbackMenuProduct(self, button):


        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuProductoTypeStore)

        #intermediary.global_variable_self.MenuProductoTypeStore.caller = button
        #intermediary.global_variable_self.MenuProductoTypeStore.open()


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeStore(self, Text):

        #print(self_store_page.ids)
        #print(instance)


        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_store_page, functions.global_variable_self.MenuProductoTypeStore, "ButtonMenuSearchingStore", Text)
        
        #self_store_page.ids.ButtonMenuSearchingStore.text = instance
        #intermediary.global_variable_self.MenuProductoTypeStore.dismiss()

    def test(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(StoreDB.ShowDataStoreModel, 0, 15)
            return_value = future.result()

            return return_value
        
    def ShowDataStoreController(self, start, end, state):

        '''
        async_result = pool.apply_async(SupplierDB.ShowData, (start, end)) # tuple of args for foo
        # do some other stuff in the main process
        return_val = async_result.get()  # get the return value from your function. 
        return return_val

        '''

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(StoreDB.ShowDataStoreModel, start,end,state)
            return_value = future.result()

            return return_value
        

    