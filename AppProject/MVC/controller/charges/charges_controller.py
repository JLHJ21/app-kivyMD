from kivymd.uix.screen import MDScreen
import MVC.controller.functions as functions

from MVC.model.charges.charges_model import ChargesDB
import concurrent.futures

#pagina de encargo
class ChargePage(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_charge_page
        self_charge_page = self

    def ChangePageChargeAddPage(self):
 
        #obtiene el self principal del kivy
        self_main = functions.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'ChargeAddPage'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Encargo - Agregar'
    
    
    def CallbackMenuCharge(self, button):
        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuTypeChargePage)

    def ShowDataChargesController(self, start, end, state):


        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(ChargesDB.ShowDataChargesModel, start,end,state)
            return_value = future.result()

            #for d in (return_value)[start + 1 :end]:
            #    print(d)

            #return return_value
        
            data = list(return_value.keys())

            for index, item in enumerate(data[1:]):
                #usar la variable de money_preference con un match y se multiplica/divide con el valor obtenido de la base de datos (valor siempre en pesos)
                profit = return_value['dato' + str(index)][0]['buy_products']

                
                #Me da el valor del producto así -> 4500.00
                #profit = functions.FunctionsKivys.TransformProfit(profit, 'float')
                #profit = functions.FunctionsKivys.ChangeCommaAndDot(profit, False)

                #new_profit = functions.FunctionsKivys.TransformMoney(profit, functions.money_preference)

                #print('aqui')
                #print(new_profit)
                #Me da el valor del producto así -> 4.500,00
                new_profit = functions.FunctionsKivys.TransformProfit(profit, 'human')
                #print(new_profit)

                return_value['dato' + str(index)][0]['buy_products'] = str(new_profit)


            return return_value  


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeCharge(self = None, Text = ""):

        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_charge_page, functions.global_variable_self.MenuTypeChargePage, "ButtonMenuSearchingCharge", Text)

