from kivymd.uix.screen import MDScreen
import MVC.controller.functions as functions
import concurrent.futures
from MVC.model.sales_history.sales_history_model import SalesHistoryDB

#PAGINA DE HISTORIAL DE VENTAS
class SalesHistoryPage(MDScreen):

    def on_pre_enter(self):

        #SalesHistoryDB.ShowDataSalesHistoryModel(0,5, '')

        if functions.have_session != True:
            functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_sales_history
        self_sales_history = self


    def CallbackMenuSalesHistory(self, button):

        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuTypeSalesHistory)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeSalesHistory(self, Text):


        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_sales_history, functions.global_variable_self.MenuTypeSalesHistory, "ButtonMenuSearchingSalesHistory", Text)

    
    def ShowDataSalesHistoryController(self, start, end, state):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(SalesHistoryDB.ShowDataSalesHistoryModel, start,end,state)
            return_value = future.result()
            return return_value    