from kivymd.uix.screen import MDScreen
from MVC.model.clients.clients_model import ClientsDB
import MVC.controller.functions as functions

class ClientAddPage(MDScreen):


    def AddNewClient(self, name, id, phone):
        
        #print(name, id, phone)
        results = ClientsDB.CreateClient(name, id, phone)
        
        if results == True:
            functions.FunctionsKivys.ChangePage('ClientsPage', 'Cliente')
        pass

    pass