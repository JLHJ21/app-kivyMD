from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

import MVC.controller.functions as functions
from MVC.model.foreign_exchange.foreign_exchange_model import ForeignExchangeDB

from MVC.controller.foreign_exchange.update.update_foreign_exchange_controller import UpdateForeignExchangePage
from kivymd.toast.kivytoast.kivytoast import toast
from kivy.app import App

from kivy.clock import Clock

#PAGINA DE DIVISAS
class ForeignExchangePage(MDScreen):

    inputDollar = StringProperty('')
    inputPeso = StringProperty('')
    inputBolivar = StringProperty('')
    lastChange = StringProperty('')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.UpdateForeignExchange()

    def on_pre_enter(self):
        
        if functions.have_session == True:
            self.UpdateForeignExchange()


        else:
            toast('No tiene una sesión activa.')
            functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')

    def UpdateMoneyPreference(self, preference):

        
        if functions.money_preference == preference:
            toast('Ya está elegido esta tasa')
        else:

            from templates.table.table import ModalsDialog, global_rv

            #Cambia la preferencia
            functions.money_preference = preference

            #OJO
            self_page = App.get_running_app().root.ids.screen_manager.get_screen('ForeignExchangePage')
            self_store = App.get_running_app().root.ids.screen_manager.get_screen('StorePage')
            self_cashier = App.get_running_app().root.ids.screen_manager.get_screen('CashierPage')

            #Obtiene los ids del recycleviewTable
            self_store_rv = self_store.ids.tableAlmacen.objecto.rv

            self_cashier_rv = self_cashier.ids.tableCashierProducts.objecto.rv
            self_cashier_shooping_rv = self_cashier.ids.tableCashierCar.objecto.rv


            #Actualiza la tabla de Almacen
            ModalsDialog.ActualizeData(global_rv[self_store_rv], self_store_rv)
            #Actualiza la tabla de Productos Cajero
            ModalsDialog.ActualizeData(global_rv[self_cashier_rv], self_cashier_rv)
            #Actualiza la tabla de Productos Cajero Shopping Cart
            ModalsDialog.ActualizeData(global_rv[self_cashier_shooping_rv], self_cashier_shooping_rv)

            ForeignExchangePage.UpdateTextPrincipalPage(self_page)

    def UpdateTextPrincipalPage(self):

        from MVC.controller.header_footer.header_footer_controller import HeaderAndFooter, self_header_and_footer

        self_main = functions.global_variable_self
        try:
            if self_main.root.ids:
                HeaderAndFooter.CallbackTypeMoney(self_header_and_footer, functions.money_preference)
                #print('if')
        except:
            pass
            #print('except')

        match functions.money_preference:
            case 'dolar':
                inputDollar = 'PREFERIDO'
                inputPeso =  'El cambio es de: 1'
                inputBolivar = 'El cambio es de: ' + str(functions.rate_bolivar)

            case 'peso':
                inputDollar = 'El cambio es de: ' + str(functions.rate_dolar)
                inputPeso =  'PREFERIDO'
                inputBolivar = 'El cambio es de: ' + str(functions.rate_bolivar)
            case 'bolivar':
                inputDollar = 'El cambio es de: ' + str(functions.rate_dolar)
                inputPeso =  'El cambio es de: 1'
                inputBolivar = 'PREFERIDO'
            
        self.lastChange = "Última actualización: " + str(functions.last_change)
        self.inputDollar = inputDollar
        self.inputPeso = inputPeso
        self.inputBolivar = inputBolivar

    def UpdateForeignExchange(self):

        #PREGUNTA A LA BASE DE DATOS, LOS VALORES
        listData = ForeignExchangeDB.GetForeignExchange()
        dolar = listData['rate_dolar']
        #peso = listData['peso']
        bolivar = listData['rate_bolivar']
        preference = listData['money_preference']
        last_change = listData['last_change']

        #ACTUALIZA LOS DATOS PARA LAS VARIABLES GLOBALES
        functions.GlobalVariables.UpdateForeignExchange(bolivar, dolar, preference, last_change)
        self.UpdateTextPrincipalPage()
        #VIEJO
        '''
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
        '''

    def ChangePageUpdateExchangeForeign(self):

        inputDolar = functions.rate_dolar
        inputBolivar = functions.rate_bolivar

        
        listTextChange = {}
        listTextChange['dolar'] = inputDolar
        listTextChange['bolivar'] = inputBolivar


        #listTextChange.extend([inputDolar, inputBolivar])

        UpdateForeignExchangePage.UpdateTextRateMoney('self', listTextChange)

        #obtiene el self principal del kivy
        self_main = functions.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'UpdateForeignExchangePage'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Modificar - Divisa'


        '''
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
        '''
        

    #Funcion al dar click al boton
    def ChangeForeignExchange(self, text):

        print('click al change')

        if functions.money_preference == text:
            toast('Hubo un error, ya existe esta moneda como preferencia.')
        else:

            result = ForeignExchangeDB.UpdateMoneyPreference(text)

            if result:
                self.UpdateTextPrincipalPage()
                toast('Se ha cambiado la preferencia monetaria.')
            else:
                toast('Hubo un error' + str(result))
        '''
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

        '''
        #self.inputDollar = Dollar
        #self.inputPeso = Peso
        #self.inputBolivar = Bolivar
