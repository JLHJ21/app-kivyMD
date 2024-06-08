from kivymd.uix.screen import MDScreen
from kivymd.toast import toast

from MVC.model.clients.clients_model import ClientsDB
import MVC.controller.functions as functions

class ClientAddPage(MDScreen):


    def AddNewClient(self, name, id, phone):
        
        #print(name, id, phone)
        results = ClientsDB.CreateClient(name, id, phone)
        
        if results == True:

            from MVC.controller.clients.clients_controller import self_clients_page
            from templates.table.table import ModalsDialog

            objecto = self_clients_page.ids.tableClient.objecto
            objectoRv = self_clients_page.ids.tableClient.objecto.rv

            #el primero es el objecto (variable objecto que lleva el widget weak), el segundo es el objecto.rv del recycleview
            ModalsDialog.ActualizeData(objecto, objectoRv)
            toast('¡Proveedor agregado con éxito!')            
            functions.FunctionsKivys.ChangePage('self', 'ClientsPage', 'Cliente')
        pass

    pass