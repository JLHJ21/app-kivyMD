from kivymd.uix.screen import MDScreen
import MVC.controller.functions as functions


#PAGINA DE PROVEEDOR
class SupplierPage(MDScreen):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_SupplierCharge
        self_SupplierCharge = self

    
    def ChangePageSupplierPage(self):

        #obtiene el self principal del kivy
        self_main = functions.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'SupplierAddPage'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Proveedor - Agregar'
    

    def CallbackMenuSupplier(self, button):

        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuTypeSupplierPage)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeSupplier(self = None, Text = ""):

        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_SupplierCharge, functions.global_variable_self.MenuTypeSupplierPage, 'ButtonMenuSearchingSupplier', Text)
