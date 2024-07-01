
from kivymd.uix.screen import MDScreen
from MVC.model.store.store_model import StoreDB
#from MVC.controller.functions import MenuAndTitleSelect, global_variable_self

import MVC.controller.functions as functions
import concurrent.futures
from kivymd.toast.kivytoast.kivytoast import toast

#PAGINA DE ALMACEN
class StorePage(MDScreen):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_store_page
        self_store_page = self


    def on_pre_enter(self):
        
        if functions.have_session != True:
            toast('No tiene una sesión activa.')
            functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')

    def CallbackMenuProduct(self, button):


        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuProductoTypeStore)

        #intermediary.global_variable_self.MenuProductoTypeStore.caller = button
        #intermediary.global_variable_self.MenuProductoTypeStore.open()


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeStore(self, Text):

        #print(self_store_page.ids)
        #print(instance)


        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_store_page, functions.global_variable_self.MenuProductoTypeStore, "ButtonMenuSearchingStore", Text)
        
        #self_store_page.ids.ButtonMenuSearchingStore.text = instance
        #intermediary.global_variable_self.MenuProductoTypeStore.dismiss()

    def test(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(StoreDB.ShowDataStoreModel, 0, 15)
            return_value = future.result()

            return return_value
        
    def ShowDataStoreController(self, start, end, state):

        '''
        async_result = pool.apply_async(SupplierDB.ShowData, (start, end)) # tuple of args for foo
        # do some other stuff in the main process
        return_val = async_result.get()  # get the return value from your function. 
        return return_val

        '''

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(StoreDB.ShowDataStoreModel, start,end,state)
            return_value = future.result()

            
            data = list(return_value.keys())

            for index, item in enumerate(data[1:]):
                #usar la variable de money_preference con un match y se multiplica/divide con el valor obtenido de la base de datos (valor siempre en pesos)
                profit = return_value['dato' + str(index)][0]['profit_product']
                #profit = functions.FunctionsKivys.ChangeCommaAndDot(profit, False)

                #Me da el valor del producto así -> 4500.00
                #profit = functions.FunctionsKivys.TransformProfit(profit, 'float')
                
                match functions.money_preference:
                    case 'bolivar':
                        new_profit = float(profit) / float(functions.rate_bolivar)
                        new_profit = f"{new_profit:.2f}"

                    case 'dolar':
                        new_profit = float(profit) / float(functions.rate_dolar)
                        new_profit = f"{new_profit:.2f}"
                    case 'peso':
                        new_profit = profit
                        #new_profit = f"{new_profit:.3f}"

                #Me da el valor del producto así -> 4.500,00
                new_profit = functions.FunctionsKivys.TransformProfit(new_profit, 'human')
                return_value['dato' + str(index)][0]['profit_product'] = str(new_profit)

            #print(return_value)

            return return_value
        

    