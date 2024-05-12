from kivymd.uix.screen import MDScreen
import MVC.controller.functions as functions

#PAGINA DE HISTORIAL DE VENTAS
class SalesHistoryPage(MDScreen):

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_sales_history
        self_sales_history = self


    def CallbackMenuSalesHistory(self, button):

        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuTypeSalesHistory)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeSalesHistory(self, Text):


        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_sales_history, functions.global_variable_self.MenuTypeSalesHistory, "ButtonMenuSearchingSalesHistory", Text)