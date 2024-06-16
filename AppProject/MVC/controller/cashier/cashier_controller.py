from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.app import App

#Archivo intermediario
import MVC.controller.functions as functions
from MVC.model.cashier.cashier_model import CashierDB
import concurrent.futures


from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.toast import toast
import re

from kivy.properties import StringProperty, NumericProperty, ObjectProperty

#Pagina de cajero

self_cashier_page = self_custom_modal = global_table_products = None
items_shopping_cart = {'characteristics': [2, 0, 5]}
#Solo permite 0-9 . y ,
regex = r'^[-,.0-9 ]+$'

class ScrollViewCashierPage(MDScrollView):
    pass

class CustomModal(MDBoxLayout): 
    idProduct = StringProperty('')
    nameProduct = StringProperty('')
    amountProduct = StringProperty('')
    profitProduct = StringProperty('')
    profitProductTransform = StringProperty('')

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_custom_modal
        self_custom_modal = self
    
    def Variables(idProduct, nameProduct, amountProduct, profitProduct):

        CustomModal.idProduct = str(idProduct)
        CustomModal.nameProduct = str(nameProduct)
        CustomModal.amountProduct = str(amountProduct)
        CustomModal.profitProduct = str(profitProduct)

        profit = str(profitProduct)
        
        #tranforma el valor obtenido, ejemplo -> 4.500,00 a 4500.00
        profit = functions.FunctionsKivys.TransformProfit(profit, 'float')


        #obtiene el valor al dividirlo/multiplicarlo con la tasa seleccionada
        profit = functions.FunctionsKivys.TransformMoney(profit)
        #transforma el valor obtenido a "vista humana"
        profit = functions.FunctionsKivys.TransformProfit(profit, 'human')

        #Me da el valor del producto así -> 4.500,00
        CustomModal.profitProductTransform = str(profit)


class CashierPage(MDScreen):

    modal_custom = ObjectProperty(None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_cashier_page
        self_cashier_page = self

    def on_pre_enter(self):

        if functions.have_session != True:
            toast('No tiene una sesión activa.')
            functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')



    def SubmitDataShoppingCart(self):

        global items_shopping_cart

        totalCost = self.ids.totalCost.text
        intTotalCost = functions.FunctionsKivys.TransformProfit(totalCost, 'float')

        idStaff = functions.idStaff
        nameStaff = functions.usernameStaff

        purchaseAmount = self.ids.inputPaid.text
        typePurchase = self.ids.ButtonMenuCashierPaymentType.text

        products = items_shopping_cart

        idClient = self.ids.idClient.text
        idObjectClient = self.ids.nameClient.name
        nameClient = self.ids.nameClient.text
        phoneClient = self.ids.phoneClient.text


        #totalMoney = 0
        

        if re.fullmatch(regex, totalCost) != None:
            
            if (len(items_shopping_cart) - 1) <= 0:
                #print('no hay items agregados')
                toast('No hay ningún producto por comprar.')
            

            if float(intTotalCost) <= 0.0:

                if idClient != '' and nameClient != '' and phoneClient != '':
                    from templates.table.table import global_rv, global_self_shoppingCart, ModalsDialog

                    if idObjectClient == '':
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(CashierDB.CreateClient, nameClient, idClient, phoneClient)
                            return_value = future.result()

                            idObjectClient = return_value['_id']

                    #purchaseAmount = functions.FunctionsKivys.TransformProfit(totalCost, 'float')
                    purchaseAmount = functions.FunctionsKivys.TransformProfit(purchaseAmount, 'float')

                    #OJO
                    match typePurchase:
                        case 'Dólar':
                            purchaseAmountOriginal =  float(purchaseAmount) * float(functions.rate_dolar)
                        case 'Peso':
                            purchaseAmountOriginal = float(purchaseAmount) * 1

                        case 'Bolívar':
                            purchaseAmountOriginal = float(purchaseAmount) * float(functions.rate_bolivar)
                    
                    #purchaseAmount = functions.FunctionsKivys.TransformProfit(purchaseAmount, 'human')
                    purchaseAmountOriginal = functions.FunctionsKivys.TransformProfit(purchaseAmountOriginal, 'human')


                    #data = list(items_shopping_cart.keys())
                    #for index, item in enumerate(data[1:]):
                        #usar la variable de money_preference con un match y se multiplica/divide con el valor obtenido de la base de datos (valor siempre en pesos)
                    #    total_price = items_shopping_cart['dato' + str(index)][0]['total_price']

                    #    print()
                    #    print('hola')
                    #    print(total_price)
                                
                    #    totalMoney = float(totalMoney) + float(total_price)
                    #    totalMoney = f"{totalMoney:.2f}"

                    #Me da el valor del producto así -> 4.500,00
                    #totalMoney = functions.FunctionsKivys.TransformProfit(totalMoney, 'human')


                    
                    CashierDB.AddPurchase(idObjectClient, nameClient, phoneClient, idClient, idStaff, nameStaff, purchaseAmount, typePurchase, products, purchaseAmountOriginal) #totalMoney) #purchaseAmountOriginal)

                    items_shopping_cart.clear()
                    items_shopping_cart = {'characteristics': [2, 0, 5]}

                    self.CleanInput([nameClient, phoneClient, idClient, purchaseAmount, totalCost])

                    #Actualiza los datos de la tabla de Carrito Productos ShoppingCart
                    ModalsDialog.ActualizeData(global_rv[global_self_shoppingCart], global_self_shoppingCart)
                    #Actualiza los datos de la tabla de Historial de Ventas SalesHistory
                    self_sales_history = App.get_running_app().root.ids.screen_manager.get_screen('SalesHistoryPage')
                    self_sales_history_rv = self_sales_history.ids.tableSalesHistory.objecto.rv

                    ModalsDialog.ActualizeData(global_rv[self_sales_history_rv], self_sales_history_rv)


                    toast('¡Compra realizada con éxito!')
                else:
                    toast('Faltan datos del cliente')

            else:
                
                toast('No se puede realizar la compra porque falta dinero por pagar.')

        else:
            toast('Hubo un error, el campo pagado solo acepta números')

    def CleanInput(self, itemClean):

        for item in itemClean:

            item = ""

            try:
                item = ""
            except:
                pass

    def UpdateTotalCost(self):

        foreign_exchange = ''
        totalCost = 0
        listPrices = 0
        totalMoneyPaid = 0

        errorPaid = 0

        moneyPaid =  self_cashier_page.ids.inputPaid.text
        typeForeignExchange = self_cashier_page.ids.ButtonMenuCashierPaymentType.text
        data = list(items_shopping_cart.keys())

        if moneyPaid == '':
            pass
        else:

            if re.fullmatch(regex, moneyPaid) == None:
                toast('Hubo un error, el campo pagado solo acepta números')
                return
            
            moneyPaid = functions.FunctionsKivys.TransformProfit(moneyPaid, 'float')
            totalMoneyPaid = moneyPaid



        #match typeForeignExchange:
        #    case 'Dólar':
        #        foreign_exchange = functions.rate_dolar
        #    case 'Peso':
        #        foreign_exchange = 1

        #    case 'Bolívar':
        #        foreign_exchange = functions.rate_bolivar

        for d in (data)[1:]:
            try:

                #guardar el valor del total_price (dado en pesos)
                profit = items_shopping_cart[d][0]['total_price']
                #tranforma el valor obtenido, ejemplo -> 4.500,00 a 4500.00
                #profit = functions.FunctionsKivys.TransformProfit(profit, 'float')
                #print(profit)

                #obtiene el valor al dividirlo/multiplicarlo con la tasa seleccionada
                profit = functions.FunctionsKivys.TransformMoney(profit, typeForeignExchange)

                #transforma el valor obtenido a "vista humana"
                #profit = functions.FunctionsKivys.TransformProfit(profit, 'human')

                #transform_money = functions.FunctionsKivys.TransformMoney(items_shopping_cart[d][0]['total_price'], typeForeignExchange)
                listPrices = float(listPrices) + float(profit)


            except:
                pass

        #CAMBIOS DEPENDIENDO DE LA MONEDA
        #listPrices = float(listPrices) * float(foreign_exchange)
        #totalMoneyPaid = float(totalMoneyPaid) * float(foreign_exchange)

        #totalCost = self_cashier_page.ids.totalCost.text.rstrip("$") 
        totalCost = float(listPrices) - float(totalMoneyPaid)
        totalCost = functions.FunctionsKivys.TransformProfit(totalCost, 'human')

        #totalCost = f"{totalCost:.3f}"
        #totalCostForeignExchange = float(totalCost)
        #totalCostForeignExchange = f"{totalCostForeignExchange:.3f}"
        
        #if float(totalCost) < 0:
        #    self_cashier_page.ids.totalCost.text = '0$'
        #else:

        self_cashier_page.ids.totalCost.text = str(totalCost)# + '$'


    def UpdateAmountShoppingCart(id_product, global_rv, global_modal_rv):

        #print(id_product)
        #self_cashier_page.AddProductToShoppingCart(global_rv, global_modal_rv, True, id_product)
        data = list(items_shopping_cart)

        for item in (data)[1:]:
            if items_shopping_cart[item][0]['_id'] == id_product:
                
                break

    def ModalAddProductToShoppingCart(typeModal):

        from templates.table.table import global_self_modal, global_id_modal, global_modal_rv, global_rv, ModalsDialog
        
        results = CashierDB.GetDataProduct(global_id_modal)

        CustomModal.Variables(results['_id'], results['name_product'], results['amount_product'], results['profit_product'])


        if typeModal == 'add':
            on_release_acept = lambda x='': self_cashier_page.AddProductToShoppingCart(global_rv, global_modal_rv)
        else:
            
            on_release_acept = lambda x='': self_cashier_page.UpdateProductToShoppingCart(global_rv, global_modal_rv, global_id_modal)
            #on_release_acept = lambda x='': self_cashier_page.AddProductToShoppingCart(global_rv, global_modal_rv, True, global_id_modal)
            #on_release_acept = lambda x='': CashierPage.UpdateAmountShoppingCart(global_id_modal, global_rv, global_modal_rv)

        #Funcion que llame base de datos y obtenga los datos del productos mediante el global_id_modal
        self_cashier_page.modal_custom = MDDialog(
                title='Agregando producto al carrito',
                #text='Por favor elija la cantidad del producto X, a comprar',
                type="custom",
                content_cls=CustomModal(),
                buttons=[
                    MDFlatButton(
                        md_bg_color="red",                     
                        text="Cancelar",
                        on_release = lambda x='': ModalsDialog.CloseDialog(self_cashier_page.modal_custom.dismiss())
                    ),
                    MDRaisedButton(
                        text="Aceptar",
                        md_bg_color="blue",
                        on_release= on_release_acept
                    ), 
                ],
            )
        self_cashier_page.modal_custom.open()

    #OJO
    def DeleteProductShoppingCart():

    
        from templates.table.table import global_id_modal, global_rv, global_self_shoppingCart, global_modal_rv, ModalsDialog

        global items_shopping_cart
        
        data = list(items_shopping_cart.keys())

        for d in (data)[1:]:

            if items_shopping_cart[d][0]['_id'] == global_id_modal:
                idProductShoppingCart = items_shopping_cart[d][0]['_id']
                amountOriginal = items_shopping_cart[d][0]['amount_original']
                del items_shopping_cart[d]
                break
        

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(CashierDB.UpdateAmountProduct, idProductShoppingCart, amountOriginal)

        CashierPage.ActualizeItemShoppingCart(global_self_shoppingCart)
        self_cashier_page.UpdateTotalCost()

        ModalsDialog.ActualizeData(global_rv[global_table_products], global_table_products)
        ModalsDialog.ActualizeData(global_rv[global_self_shoppingCart], global_self_shoppingCart)
          
    def ActualizeItemShoppingCart(self):

        global items_shopping_cart, self_custom_modal
        from templates.table.table import global_self_shoppingCart, global_rv    

        start = global_rv[global_self_shoppingCart].objecto.StartPagination
        end = global_rv[global_self_shoppingCart].objecto.StaticItemsAccountPagination

        data = list(items_shopping_cart.keys())
        #Cantidad de items que se mostrarán en el "Mostrando X-X"

        if (len(items_shopping_cart) - 1) <= 0:
            count_items = 0
        else:
            count_items = len(items_shopping_cart) - 1

        new_items = {'characteristics': [count_items, start, end]}

        for index, d in enumerate((data)[1:]):

            idProductShoppingCart = items_shopping_cart[d][0]['_id']
            nameProduct = items_shopping_cart[d][0]['name_product']
            amountWanted = items_shopping_cart[d][0]['amount_wanted']
            totalPrice = items_shopping_cart[d][0]['total_price']
            amountOriginal = items_shopping_cart[d][0]['amount_original']

            new_item = {'dato'+str(index): [{'_id': idProductShoppingCart, 'name_product': nameProduct, 'amount_wanted': amountWanted, 'total_price': totalPrice, 'amount_original': amountOriginal}]}

            new_items.update(new_item)

        items_shopping_cart.clear()
        items_shopping_cart.update(new_items)
        
    def UpdateProductToShoppingCart(self, global_rv, global_modal_rv, id_product):
        
        global items_shopping_cart, self_custom_modal
        from templates.table.table import global_self_shoppingCart, ModalsDialog

        ModalsDialog.CloseDialog(self_cashier_page.modal_custom.dismiss())

        amountWanted = self_custom_modal.ids.amountWanted.text
        amountProduct = CustomModal.amountProduct

        if amountWanted == '':
            
            toast('Hubo un error, la cantidad debe ser mayor a 0.')
            return
        elif int(amountWanted) > int(amountProduct):
            toast('Hubo un error, te pasas del producto.')
            return
        else:

            self_cashier = App.get_running_app().root.ids.screen_manager.get_screen('CashierPage')
            self_cashier_rv = self_cashier.ids.tableCashierProducts.objecto.rv

            idProduct = str(CustomModal.idProduct)
            nameProduct = CustomModal.nameProduct
            profitProduct = CustomModal.profitProduct
            amountProduct = CustomModal.amountProduct

            #Obtiene el valor que se agregara a la base de datos
            #for item in global_rv[global_modal_rv].objecto.rv.data:

            #    if item['dato']['name_product'] == nameProduct:
            #        print('a')
            #        print(item['dato']['amount_wanted'] )
                    #print(item['dato']['amount_original'])
            #        print(global_rv[global_modal_rv].objecto.rv.data)
            #        amount_discount = int(amountProduct) - int(amountWanted)

            #        break

            data = list(items_shopping_cart.keys())

            for d in (data)[1:]:

                if items_shopping_cart[d][0]['_id'] == id_product:

                    amountOriginal = items_shopping_cart[d][0]['amount_original']
                    amount_discount = int(amountOriginal) - int(amountWanted)

                    break

            print('aquii')
            print(amountOriginal)
            print(amount_discount)



            #Cambia la cantidad de produtos en la base de datos            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(CashierDB.UpdateAmountProduct, idProduct, str(amount_discount))
            
            #Actualiza los datos de la tabla de productos de cajero página
            ModalsDialog.ActualizeData(global_rv[self_cashier_rv], self_cashier_rv)

            #Me transforma el 75,85 a 75.85
            profitProduct = functions.FunctionsKivys.TransformProfit(profitProduct, 'float')
            #print()
            #Valor mas cantidad
            totalPrice = int(amountWanted) * float(profitProduct)
            #print(totalPrice)
            totalPrice = f"{totalPrice:.2f}"
            #print(totalPrice)

            start = global_rv[global_self_shoppingCart].objecto.StartPagination
            end = global_rv[global_self_shoppingCart].objecto.StaticItemsAccountPagination


            
            #OJO
            #Cantidad de items que se mostrarán en el "Mostrando X-X"
            if (len(items_shopping_cart) - 1) <= 0:
                count_items = 0
            else:
                count_items = len(items_shopping_cart) - 1

            #Comprueba si exista la llave "characteristics" en el dictionary
            if 'characteristics' in items_shopping_cart:

                items_shopping_cart['characteristics'] = [count_items, start, end]
            #Si no es así lo crea
            else:
                new_characteristics = {'characteristics': [count_items, start, end]}
                items_shopping_cart.update(new_characteristics)


            data = list(items_shopping_cart)
            
            #actualiza el valor de la cantidad del producto en carrito de compras
            for item in (data)[1:]:
                if items_shopping_cart[item][0]['_id'] == id_product:
                    #result = int(items_shopping_cart[item][0]['amount_wanted']) + int(amountWanted)
                    items_shopping_cart[item][0]['amount_wanted'] = str(amountWanted)

            #actualiza el costo total
            self_cashier_page.UpdateTotalCost()
            #actualiza los datos de la tabla de carrito de comprar
            ModalsDialog.ActualizeData(global_rv[global_self_shoppingCart], global_self_shoppingCart)

    def AddProductToShoppingCart(self, global_rv, global_modal_rv):

        global items_shopping_cart, self_custom_modal
        from templates.table.table import global_self_shoppingCart, ModalsDialog

        ModalsDialog.CloseDialog(self_cashier_page.modal_custom.dismiss())

        amountWanted = self_custom_modal.ids.amountWanted.text
        amountProduct = CustomModal.amountProduct

        if amountWanted == '':
            
            toast('Hubo un error, la cantidad debe ser mayor a 0.')
            return
        elif int(amountWanted) > int(amountProduct):
            toast('Hubo un error, te pasas del producto.')
            return
        else:

            global global_table_products
            global_table_products = global_modal_rv

            print()
            print()
            print('global')
            print(global_table_products)
            print()
            print()
            print()



            idProduct = str(CustomModal.idProduct)
            nameProduct = CustomModal.nameProduct
            profitProduct = CustomModal.profitProduct


            #Obtiene el valor que se agregara a la base de datos
            for item in global_rv[global_modal_rv].objecto.rv.data:

                if item['dato']['name_product'] == CustomModal.nameProduct:
                    amount_discount = int(item['dato']['amount_product']) - int(amountWanted)
                    break


            #Cambia la cantidad de produtos en la base de datos            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(CashierDB.UpdateAmountProduct, idProduct, str(amount_discount))
            
            #Actualiza los datos de la tabla de productos de cajero página
            ModalsDialog.ActualizeData(global_rv[global_modal_rv], global_modal_rv)


            #print('ja')

            #print(profitProduct)
            #print(functions.rate_bolivar)
            #print(functions.rate_dolar)
            
            #Me transforma el 75,85 a 75.85
            profitProduct = functions.FunctionsKivys.TransformProfit(profitProduct, 'float')

            #print(float(profitProduct))
            #print(float(profitProduct) / float(functions.rate_bolivar))
            #print(float(profitProduct) / float(functions.rate_dolar))


            #print()
            #Valor mas cantidad
            totalPrice = int(amountWanted) * float(profitProduct)
            #print(totalPrice)
            totalPrice = f"{totalPrice:.2f}"
            #print(totalPrice)

            start = global_rv[global_self_shoppingCart].objecto.StartPagination
            end = global_rv[global_self_shoppingCart].objecto.StaticItemsAccountPagination

            #OJO
            #Cantidad de items que se mostrarán en el "Mostrando X-X"
            if (len(items_shopping_cart) - 1) <= 0:
                count_items = 0
            else:
                count_items = len(items_shopping_cart) - 1

            #Comprueba si exista la llave "characteristics" en el dictionary
            if 'characteristics' in items_shopping_cart:

                items_shopping_cart['characteristics'] = [count_items, start, end]
            #Si no es así lo crea
            else:
                new_characteristics = {'characteristics': [count_items, start, end]}
                items_shopping_cart.update(new_characteristics)

            new_item = {'dato'+str(count_items): [{'_id': idProduct, 'name_product': nameProduct, 'amount_wanted': amountWanted, 'total_price': totalPrice, 'amount_original': CustomModal.amountProduct}]}

            items_shopping_cart.update(new_item)

            #actualiza el costo total
            self_cashier_page.UpdateTotalCost()
            #actualiza los datos de la tabla de carrito de comprar
            ModalsDialog.ActualizeData(global_rv[global_self_shoppingCart], global_self_shoppingCart)

    def CallbackMenuCashierPaymentType(self, button):

        functions.global_variable_self.MenuCashierPaymentType.caller = button
        functions.global_variable_self.MenuCashierPaymentType.open()

    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def CashierPaymentType(self = None, instance = ""):

        self_cashier_page.ids.ButtonMenuCashierPaymentType.text = instance
        self_cashier_page.UpdateTotalCost()
        functions.global_variable_self.MenuCashierPaymentType.dismiss()

    def ShowDataCashierProductsController(self, start, end, state):


        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(CashierDB.ShowDataCashierProductsModel, start,end,state)
            return_value = future.result()

            data = list(return_value.keys())

            for index, item in enumerate(data[1:]):
                #usar la variable de money_preference con un match y se multiplica/divide con el valor obtenido de la base de datos (valor siempre en pesos)
                profit = return_value['dato' + str(index)][0]['profit_product']

                
                #Me da el valor del producto así -> 4500.00
                profit = functions.FunctionsKivys.TransformProfit(profit, 'float')
                #profit = functions.FunctionsKivys.ChangeCommaAndDot(profit, False)

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

                #new_profit = functions.FunctionsKivys.ChangeCommaAndDot(new_profit, True)
                
                #Me da el valor del producto así -> 4.500,00
                new_profit = functions.FunctionsKivys.TransformProfit(new_profit, 'human')

                return_value['dato' + str(index)][0]['profit_product'] = str(new_profit)


            return return_value    
        
    def ShowDataCashierProductsShoppingCartController(self, start, end, state):

        from templates.table.table import global_rv, global_self_shoppingCart

        start = global_rv[global_self_shoppingCart].objecto.StartPagination
        end = global_rv[global_self_shoppingCart].objecto.StaticItemsAccountPagination

        data = list(items_shopping_cart.keys())

        #Cantidad de items que se mostrarán en el "Mostrando X-X"
        if (len(items_shopping_cart) - 1) <= 0:
            count_items = 0
        else:
            count_items = len(items_shopping_cart) - 1

        list_return = {'characteristics': [count_items, start, end]}
        data = list(items_shopping_cart.keys())

        for d in (data)[start + 1 :end]:


            #guardar el valor del total_price (dado en pesos)
            new_profit = items_shopping_cart[d][0]['total_price']

            '''
            No es necesario porque ya, viene guardado en el diccionario el precio en forma de lectura de maquina (75.85, no 75,85)
            '''
            #tranforma el valor obtenido, ejemplo -> 4.500,00 a 4500.00
            #new_profit = functions.FunctionsKivys.TransformProfit(new_profit, 'float')

            #obtiene el valor al dividirlo/multiplicarlo con la tasa seleccionada
            new_profit = functions.FunctionsKivys.TransformMoney(new_profit, functions.money_preference)

            #transforma el valor obtenido a "vista humana"
            new_profit = functions.FunctionsKivys.TransformProfit(new_profit, 'human')


            new_item = {d: [
                    {'_id': items_shopping_cart[d][0]['_id'], 
                    'name_product': items_shopping_cart[d][0]['name_product'], 
                    'amount_wanted': items_shopping_cart[d][0]['amount_wanted'], 
                    'total_price': new_profit}
                ]}

            list_return.update(new_item)


        return list_return



    def SearchClient(self, textId):
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(CashierDB.SearchClient, self,textId)
            return_value = future.result()
        
        if return_value[0] == True:

            self.ids.nameClient.name = str(return_value[1]['_id'])
            self.ids.nameClient.text = str(return_value[1]['name_client'])
            self.ids.phoneClient.text = str(return_value[1]['phone_client'])
            self.ids.idClient.icon_left = 'smart-card'
        
        else:
            
            self.ids.nameClient.text = ''
            self.ids.phoneClient.text = ''
            self.ids.idClient.icon_left = 'smart-card-off'
        

        