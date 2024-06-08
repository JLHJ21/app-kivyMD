from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

#Archivo intermediario
import MVC.controller.functions as functions
from MVC.model.cashier.cashier_model import CashierDB
import concurrent.futures


from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.toast import toast

from kivy.properties import StringProperty, NumericProperty, ObjectProperty

#Pagina de cajero

self_cashier_page = self_custom_modal = global_table_products = None
items_shopping_cart = {'characteristics': [2, 0, 5]}

class ScrollViewCashierPage(MDScrollView):
    pass

class CustomModal(MDBoxLayout): 
    idProduct = StringProperty('')
    nameProduct = StringProperty('')
    amountProduct = StringProperty('')
    profitProduct = StringProperty('')

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_custom_modal
        self_custom_modal = self
    
    def Variables(idProduct, nameProduct, amountProduct, profitProduct):

        CustomModal.idProduct = str(idProduct)
        CustomModal.nameProduct = str(nameProduct)
        CustomModal.amountProduct = str(amountProduct)
        CustomModal.profitProduct = str(profitProduct)


class CashierPage(MDScreen):

    modal_custom = ObjectProperty(None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_cashier_page
        self_cashier_page = self

    def on_pre_enter(self):

        if functions.have_session != True:
            functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')

    def SubmitDataShoppingCart(self):

        global items_shopping_cart

        totalCost = self.ids.totalCost.text
        intTotalCost = totalCost.rstrip("$")

        if float(intTotalCost) <= 0:

            if (len(items_shopping_cart) - 1) <= 0:
                #print('no hay items agregados')
                toast('No hay ningún producto por comprar.')

            else:
                idClient = self.ids.idClient.text
                
                idObjectClient = self.ids.nameClient.name
                nameClient = self.ids.nameClient.text
                phoneClient = self.ids.phoneClient.text

            
                if idClient != '' and nameClient != '' and phoneClient != '':
                    from templates.table.table import global_rv, global_self_shoppingCart, ModalsDialog

                    if idObjectClient == '':
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(CashierDB.CreateClient, nameClient, idClient, phoneClient)
                            return_value = future.result()

                            idObjectClient = str(return_value)

                    idStaff = functions.idStaff
                    nameStaff = functions.usernameStaff

                    purchaseAmount = self.ids.inputPaid.text
                    typePurchase = self.ids.ButtonMenuCashierPaymentType.text

                    products = items_shopping_cart
                    

                    CashierDB.AddPurchase(idObjectClient, nameClient, phoneClient, idClient, idStaff, nameStaff, purchaseAmount, typePurchase, products)

                    items_shopping_cart.clear()
                    items_shopping_cart = {'characteristics': [2, 0, 5]}

                    self.CleanInput([nameClient, phoneClient, idClient, purchaseAmount, totalCost])

                    ModalsDialog.ActualizeData(global_rv[global_self_shoppingCart], global_self_shoppingCart)

                    toast('¡Compra realizada con éxito!')
                else:
                    toast('Faltan datos del cliente')
            
        else:
            toast('No se puede realizar la compra porque falta dinero por pagar.')
            #print('falta dinero')

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
        moneyPaid =  self_cashier_page.ids.inputPaid.text
        typeForeignExchange = self_cashier_page.ids.ButtonMenuCashierPaymentType.text
        data = list(items_shopping_cart.keys())

        if moneyPaid != '':
            totalMoneyPaid = moneyPaid

        match typeForeignExchange:
            case 'Dólar':
                foreign_exchange = functions.global_dolar
            case 'Peso':
                foreign_exchange = functions.global_peso

            case 'Bolívar':
                foreign_exchange = functions.global_bolivar

        for d in (data)[1:]:
            try:
                listPrices = float(listPrices) + float(items_shopping_cart[d][0]['total_price'])
            except:
                pass

        #CAMBIOS DEPENDIENDO DE LA MONEDA
        listPrices = float(listPrices) * float(foreign_exchange)
        #totalMoneyPaid = float(totalMoneyPaid) * float(foreign_exchange)

        #totalCost = self_cashier_page.ids.totalCost.text.rstrip("$") 
        totalCost = float(listPrices) - float(totalMoneyPaid)
        totalCost = f"{totalCost:.3f}"
        #totalCostForeignExchange = float(totalCost)
        #totalCostForeignExchange = f"{totalCostForeignExchange:.3f}"
        
        #if float(totalCost) < 0:
        #    self_cashier_page.ids.totalCost.text = '0$'
        #else:

        self_cashier_page.ids.totalCost.text = str(totalCost) + '$'


    def ModalAddProductToShoppingCart():

        from templates.table.table import global_self_modal, global_id_modal, global_modal_rv, global_rv, ModalsDialog
        
        results = CashierDB.GetDataProduct(global_id_modal)
        CustomModal.Variables(results['_id'], results['name_product'], results['amount_product'], results['profit_product'])

        #Funcion que llame base de datos y obtenga los datos del productos mediante el global_id_modal

        ''''''
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
                        on_release= lambda x='': self_cashier_page.AddProductToShoppingCart(global_rv, global_modal_rv)
                        #text_color=self.theme_cls.primary_color,
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

        ModalsDialog.ActualizeData(global_rv[global_self_shoppingCart], global_self_shoppingCart)
        ModalsDialog.ActualizeData(global_rv[global_table_products], global_table_products)
          
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
        

    def AddProductToShoppingCart(self, global_rv, global_modal_rv):

        global items_shopping_cart, self_custom_modal
        from templates.table.table import global_self_shoppingCart, ModalsDialog

        ModalsDialog.CloseDialog(self_cashier_page.modal_custom.dismiss())

        amountWanted = self_custom_modal.ids.amountWanted.text
        amountProduct = CustomModal.amountProduct

        if amountWanted == '':
            amountWanted = 0

        for item in global_rv[global_modal_rv].objecto.rv.data:

            if item['dato']['name_product'] == CustomModal.nameProduct:
                amount_discount = int(item['dato']['amount_product']) - int(amountWanted)
                break

        if int(amountWanted) > int(amountProduct):
            print('te pasas del producto')
        else:

            global global_table_products
            global_table_products = global_modal_rv

            idProduct = str(CustomModal.idProduct)
            nameProduct = CustomModal.nameProduct
            profitProduct = CustomModal.profitProduct




            #Cambia la cantidad de produtos en la base de datos            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(CashierDB.UpdateAmountProduct, idProduct, str(amount_discount))
            
            #Actualiza los datos de la tabla de productos de cajero página
            ModalsDialog.ActualizeData(global_rv[global_modal_rv], global_modal_rv)

            totalPrice = int(amountWanted) * float(profitProduct)
            totalPrice = f"{totalPrice:.3f}"

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
            return return_value    
        
    def ShowDataCashierProductsShoppingCartController(self, start, end, state):

        characteristics = items_shopping_cart['characteristics']

        list_return = {'characteristics': characteristics}
        data = list(items_shopping_cart.keys())

        for d in (data)[start + 1 :end]:
            

            new_item = {d: [
                    #AAAAA
                    {'_id': items_shopping_cart[d][0]['_id'], 
                    'name_product': items_shopping_cart[d][0]['name_product'], 
                    'amount_wanted': items_shopping_cart[d][0]['amount_wanted'], 
                    'total_price': items_shopping_cart[d][0]['total_price']}
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
        

        