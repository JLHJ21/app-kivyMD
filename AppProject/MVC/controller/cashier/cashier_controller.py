from kivymd.uix.screen import MDScreen

#Archivo intermediario
import MVC.controller.functions as functions



#Pagina de cajero
class CashierPage(MDScreen):

    dialogShowUpdate = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_cashier_page
        self_cashier_page = self

    def CallbackMenuCashierPaymentType(self, button):

        functions.global_variable_self.MenuCashierPaymentType.caller = button
        functions.global_variable_self.MenuCashierPaymentType.open()

    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def CashierPaymentType(self = None, instance = ""):
        
        self_cashier_page.ids.ButtonMenuCashierPaymentType.text = instance
        functions.global_variable_self.MenuCashierPaymentType.dismiss()