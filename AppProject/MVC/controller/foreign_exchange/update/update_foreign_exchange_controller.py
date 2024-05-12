from kivymd.uix.screen import MDScreen
import MVC.controller.functions as functions

from MVC.model.foreign_exchange.foreign_exchange_model import ForeignExchangeDB


class UpdateForeignExchangePage(MDScreen):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        global global_foreign_exchange_update
        global_foreign_exchange_update = self

    def ChangeDataForeignExchange(self, inputDollar, inputPeso, inputBolivar):
        
        ForeignExchangeDB.UpdateForeignExchangeData(inputDollar, inputPeso, inputBolivar)

        
        #obtiene el self principal del kivy
        self_main = functions.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'ForeignExchangePage'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Divisas'
        
        pass

    def ChangeTextUpdatePage(self, listItems):

        #DOLAR
        global_foreign_exchange_update.ids.updateForeignExchangeLabelDollar.text = listItems[0] #LABEL
        global_foreign_exchange_update.ids.updateForeignExchangeTextFieldDollar.readonly = listItems[1] #TextField

        #PESO
        global_foreign_exchange_update.ids.updateForeignExchangeLabelPeso.text = listItems[2] #LABEL
        global_foreign_exchange_update.ids.updateForeignExchangeTextFieldPeso.readonly = listItems[3] #TextField

        #BOLIVAR
        global_foreign_exchange_update.ids.updateForeignExchangeLabelBolivar.text = listItems[4] #LABEL
        global_foreign_exchange_update.ids.updateForeignExchangeTextFieldBolivar.readonly = listItems[5] #TextField

        global_foreign_exchange_update.ids.TitleUpdateForeignExchange.text = listItems[6] #TextField

        #print(global_foreign_exchange_update.ids.updateForeignExchangeLabelBolivar.text)
