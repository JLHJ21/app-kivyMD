from kivymd.uix.screen import MDScreen
from kivymd.toast import toast

from kivy.properties import BooleanProperty, ObjectProperty, ListProperty, StringProperty, NumericProperty 

from MVC.model.clients.clients_model import ClientsDB
import MVC.controller.functions as functions

class ClientUpdatePage(MDScreen):

    idObject= StringProperty('')
    RV= ObjectProperty('')

    nameClient = StringProperty('')
    idClient= StringProperty('')
    phoneClient = StringProperty('')


    def on_pre_enter(self):

        from templates.table.table import global_id_modal, global_modal_rv

        self.idObject = str(global_id_modal)
        self.RV = global_modal_rv

        dataClient = ClientsDB.SearchUser(self.idObject)


        self.nameClient = dataClient['name_client']
        self.idClient= dataClient['id_client']
        self.phoneClient = dataClient['phone_client']

    def UpdateClient(self, nameClient, idClient, phoneClient):
        
        #print(name, id, phone)
        results = ClientsDB.UpdateClient(nameClient, idClient, phoneClient, self.idObject)
        
        if results == True:
            toast('¡Se ha realizado la modificación con éxito!')
            functions.FunctionsKivys.ChangePage('self', 'ClientsPage', 'Cliente')
        else:
            toast('Hubo un error ' + results)
    