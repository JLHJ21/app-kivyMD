from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

import MVC.controller.functions as functions
from MVC.model.foreign_exchange.foreign_exchange_model import ForeignExchangeDB

from MVC.controller.foreign_exchange.update.update_foreign_exchange_controller import UpdateForeignExchangePage

#PAGINA DE DIVISAS
class ForeignExchangePage(MDScreen):

    inputDollar = StringProperty(None)
    inputPeso = StringProperty(None)
    inputBolivar = StringProperty(None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.UpdateForeignExchange()


    def on_pre_enter(self):
        self.UpdateForeignExchange()
        

    def UpdateForeignExchange(self):
        listData = ForeignExchangeDB.ChangePreferenceExchangeForeign()


        functions.GlobalVariables.AddForeignExchange(listData[2], listData[1], listData[0])

        match (listData[3]):
            case 'dolar':
                    
                self.inputDollar = 'PREFERIDO'
                self.inputPeso = f'Dólar a Peso: {listData[0]}$ == {listData[1]}$$'
                self.inputBolivar = f'Dólar a Bolívar: {listData[0]}$ == {listData[2]}bs'

            case 'peso':
                    
                self.inputDollar = f'Peso a Dólar: {listData[0]}$$ == 1$'
                self.inputPeso = 'PREFERIDO'
                self.inputBolivar = f'Peso a Bolívar: {listData[1]}$$ == {listData[2]}bs'

            case 'bolivar':
                    
                self.inputDollar = f'Bolívar a Dolar: {listData[0]}bs == 1$'
                self.inputPeso = f'Bolívar a Peso: 10bs == 1000$$'
                self.inputBolivar = 'PREFERIDO'

    def ChangePageUpdateExchangeForeign(self):


        if self.inputDollar == 'PREFERIDO':

            title = 'Modificar tasa de cambio del DÓLAR'

            #Dolar
            inputLabel1 = 'Cambio de dólar a dólar:'
            stateInputLabel1 = True
            
            #Peso
            inputLabel2 = 'Cambio de dólar a peso:'
            stateInputLabel2 = False

            #Bolivar
            inputLabel3 = 'Cambio de dólar a bolívar:'
            stateInputLabel3 = False

        elif self.inputPeso == 'PREFERIDO':

            title = 'Modificar tasa de cambio del PESO'

            #Dolar
            inputLabel1 = 'Cambio de peso a dólar:'
            stateInputLabel1 = False

            #Peso
            inputLabel2 = 'Cambio de peso a peso:'
            stateInputLabel2 = True

            #Bolivar
            inputLabel3 = 'Cambio de peso a bolívar:'
            stateInputLabel3 = False

        elif self.inputBolivar == 'PREFERIDO':

            title = 'Modificar tasa de cambio del BOLÍVAR'

            #Dolar
            inputLabel1 = 'Cambio de bolívar a dólar:'
            stateInputLabel1 = False
            
            #Peso
            inputLabel2 = 'Cambio de bolívar a peso:'
            stateInputLabel2 = False

            #Bolivar
            inputLabel3 = 'Cambio de bolívar a bolívar:'
            stateInputLabel3 = True

        
        listTextChange = []

        listTextChange.extend([inputLabel1, stateInputLabel1, inputLabel2, stateInputLabel2, inputLabel3, stateInputLabel3, title])


        
        

        UpdateForeignExchangePage.ChangeTextUpdatePage('self', listTextChange)

        #obtiene el self principal del kivy
        self_main = functions.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'UpdateForeignExchangePage'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Modificar - Divisa'



    def ChangeForeignExchange(self, text):

        match (text):
            case 'dolar':
                if self.inputDollar == 'PREFERIDO':
                    pass
                else:
                    listData = ForeignExchangeDB.ChangePreferenceExchangeForeign(text)

                    self.inputDollar = 'PREFERIDO'
                    self.inputPeso = f'Dólar a Peso: {listData[0]}$ == {listData[1]}$$'
                    self.inputBolivar = f'Dólar a Bolívar: {listData[0]}$ == {listData[2]}bs'

            case 'peso':
                if self.inputPeso == 'PREFERIDO':
                    pass
                else:
                    listData = ForeignExchangeDB.ChangePreferenceExchangeForeign(text)

                    self.inputDollar = f'Peso a Dólar: {listData[0]}$$ == 1$'
                    self.inputPeso = 'PREFERIDO'
                    self.inputBolivar = f'Peso a Bolívar: {listData[1]}$$ == {listData[2]}bs'
            
            case 'bolivar':

                if self.inputBolivar == 'PREFERIDO':
                    pass
                else:
                    listData = ForeignExchangeDB.ChangePreferenceExchangeForeign(text)
                    
                    self.inputDollar = f'Bolívar a Dolar: {listData[0]}bs == 1$'
                    self.inputPeso = f'Bolívar a Peso: {listData[1]}bs == 1000$$'
                    self.inputBolivar = 'PREFERIDO'

            case _:
                print('Error')


        #self.inputDollar = Dollar
        #self.inputPeso = Peso
        #self.inputBolivar = Bolivar
