from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

#Archivo intermediario
import MVC.controller.functions as functions
from MVC.model.cashier.cashier_model import CashierDB
import concurrent.futures


from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import StringProperty, NumericProperty, ObjectProperty

#Pagina de cajero

self_cashier_page = self_custom_modal = None
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

        CustomModal.idProduct = idProduct
        CustomModal.nameProduct = nameProduct
        CustomModal.amountProduct = amountProduct
        CustomModal.profitProduct = profitProduct


class CashierPage(MDScreen):

    modal_custom = ObjectProperty(None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_cashier_page
        self_cashier_page = self

    def ModalAddProductToShoppingCart():

        from templates.table.table import global_self_modal, global_id_modal, global_modal_rv, global_rv, ModalsDialog

        #print('AQUI')

        #print(global_rv[global_modal_rv].objecto.rv.data)
        

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

            if items_shopping_cart[d][0]['name_product'] == global_id_modal:
                del items_shopping_cart[d]
                break

        print()
        print(CustomModal.amountProduct)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(CashierDB.UpdateAmountProduct, global_id_modal, CustomModal.amountProduct)

        ModalsDialog.ActualizeData(global_rv[global_self_shoppingCart], global_self_shoppingCart)
        #OJO
        #ModalsDialog.ActualizeData(global_rv[global_modal_rv], global_modal_rv)

            
            
        pass

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

                #print('ENCONTRADO COINCIDENCIA')
                #print(item['dato']['amount_product'])
                #print()
                #item['dato']['amount_product'] = int(item['dato']['amount_product']) - int(CustomModal.amountProduct)
                #print(int(CustomModal.amountProduct))
                amount_discount = int(item['dato']['amount_product']) - int(amountWanted)
                #print(item['dato']['name_product'])
                #print(item['dato']['amount_product'])

                break

        if int(amountWanted) > int(amountProduct):
            print('te pasas del producto')
        else:

            idProduct = CustomModal.idProduct
            nameProduct = CustomModal.nameProduct
            profitProduct = CustomModal.profitProduct

            #Cambia la cantidad de produtos en la base de datos            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(CashierDB.UpdateAmountProduct, CustomModal.nameProduct, str(amount_discount))
            
            #Actualiza los datos de la tabla de productos de cajero página
            ModalsDialog.ActualizeData(global_rv[global_modal_rv], global_modal_rv)

            totalPrice = int(amountWanted) * float(profitProduct)
            totalPrice = f"{totalPrice:.3f}"

            start = global_rv[global_self_shoppingCart].objecto.StartPagination
            end = global_rv[global_self_shoppingCart].objecto.StaticItemsAccountPagination

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


            new_item = {'dato'+str(count_items): [{'_id': idProduct, 'name_product': nameProduct, 'amount_wanted': amountWanted, 'total_product': totalPrice}]}

            items_shopping_cart.update(new_item)
            
            ModalsDialog.ActualizeData(global_rv[global_self_shoppingCart], global_self_shoppingCart)

    def CallbackMenuCashierPaymentType(self, button):

        functions.global_variable_self.MenuCashierPaymentType.caller = button
        functions.global_variable_self.MenuCashierPaymentType.open()

    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def CashierPaymentType(self = None, instance = ""):
        
        self_cashier_page.ids.ButtonMenuCashierPaymentType.text = instance
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
                    {'_id': items_shopping_cart[d][0]['name_product'], 
                    'name_product': items_shopping_cart[d][0]['name_product'], 
                    'amount_wanted': items_shopping_cart[d][0]['amount_wanted'], 
                    'total_product': items_shopping_cart[d][0]['total_product']}
                ]}

            list_return.update(new_item)

        return list_return




    def SearchClient(self, textId):
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(CashierDB.SearchClient, self,textId)
            return_value = future.result()
        
        if return_value[0] == True:

            self.ids.nameClient.text = return_value[1]['name_client']
            self.ids.phoneClient.text = return_value[1]['phone_client']
            self.ids.idClient.icon_left = 'smart-card'
        
        else:
            
            self.ids.nameClient.text = ''
            self.ids.phoneClient.text = ''
            self.ids.idClient.icon_left = 'smart-card-off'
        

        