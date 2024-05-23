from kivymd.uix.screen import MDScreen
import MVC.controller.functions as functions
from MVC.model.clients.clients_model import ClientsDB

import concurrent.futures


#PAGINA DEL CLIENTE
class ClientsPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_ClientsPage
        self_ClientsPage = self


    def CallbackMenuClients(self, button):

        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuTypeClientsPage)


    def ChangePageClientPage(self):

        functions.FunctionsKivys.ChangePage('ClientAddPage', 'Cliente - Agregar')
        

    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeClients(self = None, Text = ""):
        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_ClientsPage, functions.global_variable_self.MenuTypeClientsPage, "ButtonMenuSearchingClient", Text)


    def ShowDataClientsController(self, start, end, state):

        '''
        async_result = pool.apply_async(SupplierDB.ShowData, (start, end)) # tuple of args for foo
        # do some other stuff in the main process
        return_val = async_result.get()  # get the return value from your function. 
        return return_val

        '''

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(ClientsDB.ShowData, start,end,state)
            return_value = future.result()

            return return_value
        