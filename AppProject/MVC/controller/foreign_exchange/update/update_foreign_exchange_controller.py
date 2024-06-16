from kivymd.uix.screen import MDScreen
import MVC.controller.functions as functions

from MVC.model.foreign_exchange.foreign_exchange_model import ForeignExchangeDB
from kivymd.toast.kivytoast.kivytoast import toast


class UpdateForeignExchangePage(MDScreen):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        global global_foreign_exchange_update
        global_foreign_exchange_update = self

    def UpdateRateMoney(self, dolar, bolivar):

        #VALIDACIONES
        #Bolivar
        if bolivar == '':
            toast('Hubo un error, el campo bolivar está vacío')
        #Dolar
        elif dolar == '':
            toast('Hubo un error, el campo dolar está vacío')
        else:
            errorBolivar = errorDolar = 0

            ###########

            #revisa si es numero el inputBolivar
            #es int?
            try:
                bolivar = int(bolivar)
            except:
                errorBolivar += 1

                #es float?    
                try:
                    bolivar = float(bolivar)
                    errorBolivar = 0
                except:
                    errorBolivar += 1

            if errorBolivar > 0:
                toast('Hubo un error, el campo dolar solo acepta números')
                return
                
            ###########

            #revisa si es numero el inputDolar
            #es int?
            try:
                dolar = int(dolar)
            except:
                errorDolar += 1
                
                #es float?    
                try:
                    dolar = float(dolar)
                    errorDolar = 0
                except:
                    errorDolar += 1

            if errorDolar > 0:
                toast('Hubo un error, el campo dolar solo acepta números')
                return
            
            ###########
          
            print('paso los try')
            #Actualiza el dinero segun lo escrito en el input
            result = ForeignExchangeDB.UpdateRateMoney(str(dolar), str(bolivar))

            if result == True:
            
                #obtiene el self principal del kivy
                self_main = functions.global_variable_self
                #cambia segun la pagina querida
                self_main.root.ids.screen_manager.current = 'ForeignExchangePage'
                #cambia el titulo del menu de arriba segun el nombre que queramos
                self_main.root.ids.toolbar.title = 'Divisas'
            else:
                toast('Hubo un error' + str(result))

        '''
        ForeignExchangeDB.UpdateForeignExchangeData(inputDollar, inputPeso, inputBolivar)
        '''

        
        

    def UpdateTextRateMoney(self, listItems):

        #DOLAR
        global_foreign_exchange_update.ids.inputUpdateDolar.text = listItems['dolar'] #LABEL
        #global_foreign_exchange_update.ids.updateForeignExchangeTextFieldDollar.readonly = listItems[1] #TextField

        #PESO
        #global_foreign_exchange_update.ids.updateForeignExchangeLabelPeso.text = listItems[2] #LABEL
        #global_foreign_exchange_update.ids.updateForeignExchangeTextFieldPeso.readonly = listItems[3] #TextField

        #BOLIVAR
        global_foreign_exchange_update.ids.inputUpdateBolivar.text = listItems['bolivar'] #LABEL
        #global_foreign_exchange_update.ids.updateForeignExchangeTextFieldBolivar.readonly = listItems[5] #TextField

        #global_foreign_exchange_update.ids.TitleUpdateForeignExchange.text = listItems[6] #TextField

        #print(global_foreign_exchange_update.ids.updateForeignExchangeLabelBolivar.text)
