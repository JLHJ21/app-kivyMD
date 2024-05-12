from kivymd.uix.screen import MDScreen
import MVC.controller.functions as functions


#PAGINA DEL CLIENTE
class ClientsPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_ClientsPage
        self_ClientsPage = self


    def CallbackMenuClients(self, button):

        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuTypeClientsPage)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeClients(self = None, Text = ""):
        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_ClientsPage, functions.global_variable_self.MenuTypeClientsPage, "ButtonMenuSearchingClient", Text)
