from kivymd.uix.screen import MDScreen
import MVC.controller.functions as functions

from MVC.model.charges.charges_model import ChargesDB
import concurrent.futures

#pagina de encargo
class ChargePage(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_charge_page
        self_charge_page = self

    def ChangePageChargeAddPage(self):

        #obtiene el self principal del kivy
        self_main = functions.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'ChargeAddPage'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Encargo - Agregar'
    
    
    def CallbackMenuCharge(self, button):
        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuTypeChargePage)

    def ShowDataChargesController(self, start, end, state):


        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(ChargesDB.ShowDataChargesModel, start,end,state)
            return_value = future.result()

            return return_value


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeCharge(self = None, Text = ""):

        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_charge_page, functions.global_variable_self.MenuTypeChargePage, "ButtonMenuSearchingCharge", Text)

