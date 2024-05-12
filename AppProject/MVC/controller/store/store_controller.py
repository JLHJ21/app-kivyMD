
from kivymd.uix.screen import MDScreen
#from MVC.controller.functions import MenuAndTitleSelect, global_variable_self

import MVC.controller.functions as functions

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

    