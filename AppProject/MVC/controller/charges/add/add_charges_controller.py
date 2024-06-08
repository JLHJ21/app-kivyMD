from kivy.metrics import dp
from functools import partial
import os


from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButton, MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
#from kivymd.uix.selectioncontrol import MDSwitch, MDCheckbox
from kivymd.toast import toast

#from kivy.app import App

from MVC.model.charges.charges_model import ChargesDB
import MVC.controller.functions as functions

from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty, NumericProperty, BooleanProperty #ObjectProperty
import concurrent.futures
#from kivy.uix.recycleview import RecycleView
#from kivymd.uix.filemanager import MDFileManager

import weakref

only_one_time_call = False
self_page = None

class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()


#TextField del widget Ganancias, Compras On_Text
#https://stackoverflow.com/a/47581657/20676567
class TextInputBuyAndProfit(MDTextField):

    max_characters = NumericProperty(0)

    def __init__(self, **kwargs):
        super(TextInputBuyAndProfit, self).__init__(**kwargs)

    def on_text(self, instance, text):
        ChargeAddPage.updateNumberTextChargeNew(self)

    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= self.max_characters and self.max_characters > 0:
            substring = ""
        MDTextField.insert_text(self, substring, from_undo)

class TextInputProductName(MDTextField):

    verificationProduct = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(TextInputProductName, self).__init__(**kwargs)

    def on_text(self, instance, text):
        #print(text)
        #pass
        #print(instance.icon_left)
        ChargeAddPage.ChangeIconProduct(self, instance)


class ChargeAddPage(MDScreen):

    NewLabelsList = {}

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_page
        self_page = self

    #Funciones llamadas al iniciar
    def onPreEnterFunctions(self):

        global only_one_time_call
        
        if only_one_time_call == False:

            self.list_suppliers()
            self.onReleaseSwitch()

            only_one_time_call = True
    
    def onReleaseSwitch(self):
        self.ids.SwitchChargeAdd.on_release = partial(self.CheckProductExist, self.ids.idProducto)

    #MENU DE PROVEEDORES
    def SelectItem(self, nameSupplier, nameID):
        
        self.ids.searchingSupplier.text = str(nameSupplier)
        self.ids.searchingSupplier.name = str(nameID)

        #self.ids.searchingSupplier.icon_left = 'account-star'

        #Cambiar altura del RecycleView
        self.ids.rvV.height = dp(0)
        self.ids.rvV.data = []

    def list_suppliers(self, text=""):

        #Cambiar altura del RecycleView
        self.ids.rvV.height = dp(100)

        def add_icon_item(text, name, zero_items):

            if zero_items == True:
                icon = "account-eye"
                callback = lambda x='a': self.SelectItem(text, name)

            elif zero_items == False:
                icon = "account-cancel"
                callback = lambda x='a': x

            #print(App.get_running_app().get_screen('ChargeAddPage'))#.root.get_screen('ChargeAddPage').ids.rv.data )
            
            self.ids.rvV.data.append(
                    {
                        "viewclass": "CustomOneLineIconListItem",
                        "icon": icon,
                        "text": text,
                        "name": name,
                        "on_release": callback
                    }
                )

        self.ids.rvV.data = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(ChargesDB.GetDataSupplier, text)
            return_value = future.result()


        if (len(return_value)) <= 0:
            
            text = 'No hay algún proveedor registrado con el nombre que escribiste.'
            name = 'None'
            add_icon_item(text, name, False)
        else:

            for item in return_value:

                text = return_value[item]['name_supplier']
                name = return_value[item]['_id']

                add_icon_item(text, name, True)

    #####################
    #Funcion de las imagenes
    #Abre el seleccionador
    def file_manager_open(self, instance, firstItem):
        self.firstItem = firstItem
        self.instance = instance
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        #self.manager_open = True

    #Archivo seleccionado
    def select_path(self, path_image: str):

        #Cambia la pagina
        self.manager.current = 'ChargeAddPage'
        
        name_image = os.path.basename(path_image)

        extension = name_image.split('.')
        name_image_5_letters = name_image[:5]

        name = str(name_image_5_letters) + '...' + str(extension[1])


        if self.firstItem == True:
            print('try')
            self.instance.parent.parent.children[2].text = name
            self.instance.parent.parent.children[2].name = name_image
        else:
            print('except')
            print( self.instance.parent.children[2].text)
            self.instance.parent.children[2].text = name
            self.instance.parent.children[2].name = name_image

        self.exit_manager()

    #Permite cerrar el seleccionador
    def exit_manager(self, *args):

        self.manager.current = 'ChargeAddPage'
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def ChangeIconProduct(self, instance):
        #print(instance)
        instance.icon_left = 'alpha-p-circle-outline'
        instance.verificationProduct = False

    
    def CheckProductExist(self, instance):

        existProduct = ChargesDB.ExistProduct(instance.text)

        if existProduct == True:

            toast('Existe el producto, se actualizaran sus datos.')
            instance.icon_left = 'alpha-v-circle-outline'
            instance.verificationProduct = True

            
        else:

            toast('No existe el producto, se crearán sus datos.')
            instance.icon_left = 'alpha-n-circle-outline'
            instance.verificationProduct = False


    #####################
    #Producto nuevo, opciones
    #Agrega widget/input al dar click al boton Nuevo/Viejo
    '''
    def on_switch_on(self, instance, newItem, firstItem):

        
        self.file_manager = MDFileManager(
                exit_manager=self.exit_manager, 
                select_path=self.select_path,
                preview=True,
                icon_selection_button="pencil",
            )

        NewLabels = MDRectangleFlatButton(
            text= 'Imagen',
            valign= 'center',
            rounded_button= True,
            pos_hint={'center_x':0.5, 'center_y':1},
            on_release= lambda x: self.file_manager_open(instance, firstItem)
        )
        
        match newItem:
            case True:
                #Cambia el texto del boton
                instance.text = 'Viejo'
                
                #Agrega el widget del boton Nuevo/Viejo, a una list para lograr
                dictionaryWidget = {instance : NewLabels}
                self.NewLabelsList.update(dictionaryWidget)

                if firstItem == True:

                    #Cambia el on click o on_release del mismo
                    instance.on_release = lambda x='a': self.on_switch_on(instance, False, True)
                    
                    #Cambia la cantidad de columnas que tendrá
                    instance.parent.parent.cols = int(instance.parent.parent.cols) + 1
                    #Lo añade al widget padre padre, en la posicion 2, es decir, despues del boton de Nuevo/Viejo
                    instance.parent.parent.add_widget(NewLabels, 2)

                else:

                    #Cambia el on click o on_release del mismo
                    instance.on_release = lambda x='a': self.on_switch_on(instance, False, False)

                    #Cambia la cantidad de columnas que tendrá
                    instance.parent.cols = int(instance.parent.cols) + 1
                    #Lo añade al widget padre padre, en la posicion 2, es decir, despues del boton de Nuevo/Viejo
                    instance.parent.add_widget(NewLabels, 2)


            case False:
                instance.text = 'Nuevo'


                if firstItem == True:

                    #Cambia el on click o on_release del mismo
                    instance.on_release = lambda x='a': self.on_switch_on(instance, True, True)
                    
                    #Cambia la cantidad de columnas que tendrá
                    instance.parent.parent.cols = int(instance.parent.parent.cols) - 1
                    #Lo añade al widget padre padre, en la posicion 2, es decir, despues del boton de Nuevo/Viejo

    
                    #Elimina el widget
                    instance.parent.parent.remove_widget(self.NewLabelsList[instance])
                else:

                    #Cambia el on click o on_release del mismo
                    instance.on_release = lambda x='a': self.on_switch_on(instance, True, False)

                    #Cambia la cantidad de columnas que tendrá
                    instance.parent.cols = int(instance.parent.cols) - 1
                    #Elimina del widget padre padre, en la posicion 2, es decir, despues del boton de Nuevo/Viejo

                    
                    #Elimina el widget
                    instance.parent.remove_widget(self.NewLabelsList[instance])
    '''

    #Elimina el widget
    def DeleteItemCharge(self):

        #Elimina el último item nuevo producto
        self.ids.BoxLayoutChargeAdd.remove_widget(self.ids.BoxLayoutChargeAdd.children[0])

        try:
            #Creacion de widget de eliminar producto
            NewButton = MDFloatingActionButton(

                    icon= "account-plus",
                    type= "small",
                    #on_release= self.AddItemCharge(),
                    on_release= lambda x='Item configuracion': self.AddItemCharge('NewGridName', 'NewButtonAddItem'),
                    elevation= 0,
                    pos_hint= {'center_x': .5, 'center_y': .5}
                )

            # Remueve el Button de añadir producto
            self.ids.BoxLayoutChargeAdd.children[0].remove_widget(self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem)

            #Añade el nuevo Button para eliminar producto
            self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButton)
            
            #Le agrega un id al nuevo Button
            self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton)

            if len(self.ids.BoxLayoutChargeAdd.children) >= 2:
                NewButton = MDFloatingActionButton(

                        icon= "delete",
                        type= "small",
                        #on_release= self.AddItemCharge(),
                        on_release= lambda x='': self.DeleteItemCharge(),
                        elevation= 0,
                        pos_hint= {'center_x': .5, 'center_y': .5}
                    )

                #Actualiza numero de columnas
                self.ids.BoxLayoutChargeAdd.children[1].cols =  int(self.ids.BoxLayoutChargeAdd.children[1].cols) + 1
                #Lo añade al Padre
                self.ids.BoxLayoutChargeAdd.children[1].add_widget(NewButton)
                #Se le da un identificador al widget boton de eliminar
                self.ids.BoxLayoutChargeAdd.children[1].ids.NewButtonAddItem = weakref.ref(NewButton)
                #print('hay mas')
            #else:
            #    print('NOOO hay mas')
        except AttributeError:

            #Creacion de widget de eliminar producto
            NewButton = MDFloatingActionButton(

                    icon= "account-plus",
                    type= "small",
                    #on_release= self.AddItemCharge(),
                    on_release= lambda x='Item configuracion': self.AddItemCharge('NewGridName', 'NewButtonAddItem'),
                    elevation= 0,
                    pos_hint= {'center_x': .5, 'center_y': .5}
                )

            
            #Actualiza numero de columnas
            self.ids.BoxLayoutChargeAdd.children[0].cols = int(self.ids.BoxLayoutChargeAdd.children[1].cols) + 1

            #Añade el nuevo Button para eliminar producto
            self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButton)
            
            #Le agrega un id al nuevo Button
            self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton)
            pass

    #CREACION DE NUEVOS PRODUCTOS INPUTS
    def AddItemCharge(self, ParentWidget, ChildrenWidget):

        #remueve el boton de añadir
        try:
            self.ids[ParentWidget].remove_widget(self.ids[ChildrenWidget])
            #self.ids[ParentWidget].cols = 5

            NewButtonDelete = MDFloatingActionButton(
                    icon= "delete",
                    type= "small",
                    #on_release= self.AddItemCharge(),
                    on_release= lambda x='': self.DeleteItemCharge(),
                    elevation= 0,
                    pos_hint= {'center_x': .5, 'center_y': .5}
                )
            
        
            #Lo añade al Padre
            self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButtonDelete)
            #Se le da un identificador al widget boton de eliminar
            self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButtonDelete)
    
        #Permite que se elimine usando los "weakref"
        except KeyError:

            if len(self.ids.BoxLayoutChargeAdd.children) == 1:

                self.ids.BoxLayoutChargeAdd.children[0].remove_widget(self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem)
            

                #Creacion del widget boton para eliminar producto
                NewButton2 = MDFloatingActionButton(

                        icon= "delete",
                        type= "small",
                        #on_release= self.AddItemCharge(),
                        on_release= lambda x='': self.DeleteItemCharge(),
                        elevation= 0,
                        pos_hint= {'center_x': .5, 'center_y': .5}
                    )


                #Lo añade al Padre
                self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButton2)
                #Se le da un identificador al widget boton de eliminar
                self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton2)

            #self.ids.BoxLayoutChargeAdd.children[0].cols = 5
            
            #Si la cantidad de items es mayor a 2, entonces me eliminas del antepenultimo item el boton de eliminar o agregar
            if len(self.ids.BoxLayoutChargeAdd.children) >= 2:
                print('if')
                self.ids.BoxLayoutChargeAdd.children[1].cols = int(self.ids.BoxLayoutChargeAdd.children[1].cols) - 1
                self.ids.BoxLayoutChargeAdd.children[1].remove_widget(self.ids.BoxLayoutChargeAdd.children[1].ids.NewButtonAddItem)


                #Remueve el boton de añadir del último item
                self.ids.BoxLayoutChargeAdd.children[0].remove_widget(self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem)

                #Creacion del widget boton para eliminar producto
                NewButton2 = MDFloatingActionButton(

                        icon= "delete",
                        type= "small",
                        #on_release= self.AddItemCharge(),
                        on_release= lambda x='': self.DeleteItemCharge(),
                        elevation= 0,
                        pos_hint= {'center_x': .5, 'center_y': .5}
                    )


                #Lo añade al Padre
                self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButton2)
                #Se le da un identificador al widget boton de eliminar
                self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton2)


        #####
        ##CREACION DE WIDGET GRIDLAYOUT
        #Crea el MDGridLayout donde se guardará todo
        NewGridLayout = MDGridLayout(
                cols= 6,
                spacing= dp(20),
                padding= [dp(1), dp(5), dp(1), dp(1)],
                
                size_hint_y= None,
                height= dp(60)
            )
                
                

        #Se añade el widget MDGridLayout al MDBoxLayout existente en kivy
        self.ids.BoxLayoutChargeAdd.add_widget(NewGridLayout)

        #NOMBRE DEL NUEVO GRID Y BUTTON
        NewGridName = 'NewGrid' + str(len(self.ids.BoxLayoutChargeAdd.children))

        #Se le añade un ID al nuevo MDGridLayout
        self.ids.BoxLayoutChargeAdd.ids[NewGridName] = weakref.ref(NewGridLayout)


        #####
        ##CREACION DE LOS INPUTS WIDGET TEXTFIELD
        #Crea lista de los nombre de los MDLabel que se crearan
        itemListLabel = ['Producto', 'Cantidad', 'Compra', 'Ganancia']
        #onText = None

        #For loop que creará los MDlabel segun el array itemListLabel
        for index, item in enumerate(itemListLabel):

            idNewLabels = 'id'+ str(item)
            match index:
                case 0:
                    #crea el widget
                    NewLabels = TextInputProductName(
                            mode= 'rectangle',
                            text= '',
                            hint_text= item,

                            max_text_length= 35,
                            write_tab= False,
                            
                            verificationProduct= False,
                            icon_left= 'alpha-p-circle-outline',
                            required= True
                        )
                case 1:
                    #crea el widget
                    NewLabels = MDTextField(
                            mode= 'rectangle',
                            text= '',
                            hint_text= item,

                            max_text_length= 10,
                            input_filter= 'int',
                            write_tab= False,
                            required= True

                        
                        )
                case 2:
                    #onText = 'compra'

                    #crea el widget de compra
                    NewLabels = TextInputBuyAndProfit(
                            max_characters=10,
                            mode= 'rectangle',
                            text= '',
                            hint_text= item,
                            max_text_length= 10,
                            input_filter= 'float',
                            write_tab= False,
                            required= True

                        )
                case 3:
                    #onText = 'ganancia'
                    #crea el widget de ganancia
                    NewLabels = TextInputBuyAndProfit(
                            max_characters=10,

                            mode= 'rectangle',
                            text= '',
                            hint_text= item,
                            max_text_length= 10,
                            input_filter= 'float',
                            write_tab= False,
                            required= True
                        )
            
            #Lo añade al grid creado desde el comienzo
            NewGridLayout.add_widget(NewLabels)
            #Permite que al escribir en el input de precio, permita activar la funcion changeTextItemBuy
            #en caso tal de no hacerlo así y colocarlo en el widget, no funcionará
        
            #Se le añade un ID al nuevo Layout widget
            self.ids.BoxLayoutChargeAdd.children[0].ids[idNewLabels] = weakref.ref(NewLabels)

            '''
            match onText:
            
                case 'producto':
                    NewLabels.bind(text = print('ok'))
                case _:
                    pass
            '''
        
        #####
        ##CREACION DEL INPUT WIDGET BUTTON NUEVO/VIEJO
        NewItemButton = MDRectangleFlatButton(
            text= 'Buscar item',
            valign= 'center',
            rounded_button= True,
            pos_hint={'center_x':0.5, 'center_y':1},
            #on_release= lambda x:  print('a')
        )

        #Se añade EL BOTON AL GRIDLAYOUT
        NewGridLayout.add_widget(NewItemButton)

        
        #####
        ##CREACION DEL BOTON WIDGET PARA AGREGAR MÁS ITEMS

        #Se crea boton para poder añadir otro item
        NewButton = MDFloatingActionButton(
                icon= "account-plus",
                type= "small",
                #on_release= self.AddItemCharge(),
                on_release= lambda x='Item configuracion': self.AddItemCharge('NewGridName', 'NewButtonAddItem'),
                elevation= 0,
                pos_hint= {'center_x': .5, 'center_y': .5}
            )


        #Se añade el nuevo boton al MDGridLayout Padre
        NewGridLayout.add_widget(NewButton)
        
        #Se le añade el ID al nuevo boton 'añadir producto'
        self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton)

        buttonItemNew = self.ids.BoxLayoutChargeAdd.children[0].children[1]
        textInput = self.ids.BoxLayoutChargeAdd.children[0].children[-1]
        
        buttonItemNew.on_release = lambda x='a': self.CheckProductExist(textInput)

    #Cambia número de ganancias, compras y total al escribir algún on_key en los inputs
    def updateNumberTextChargeNew(self, *args):

        totalProfitMoney = 0
        totalBuyMoney = 0

        profitProducts = 0
        amountProducts = 0
        buyProducts = 0

        for index, i in enumerate(self_page.ids.BoxLayoutChargeAdd.children):

            try:

                #Compra
                if self_page.ids.BoxLayoutChargeAdd.children[index].ids.idCompra.text == '':
                    buyProducts = 0
                else:
                    buyProducts = float(self_page.ids.BoxLayoutChargeAdd.children[index].ids.idCompra.text)

                #Ganancia
                if self_page.ids.BoxLayoutChargeAdd.children[index].ids.idGanancia.text == '':
                    profitProducts = 0
                else:
                    profitProducts = float(self_page.ids.BoxLayoutChargeAdd.children[index].ids.idGanancia.text)

                #Cantidad
                if self_page.ids.BoxLayoutChargeAdd.children[index].ids.idCantidad.text == '':
                    amountProducts = 0
                else:
                    amountProducts = float(self_page.ids.BoxLayoutChargeAdd.children[index].ids.idCantidad.text)

                #else:
                #    totalMoney = float(self_page.ids.BoxLayoutChargeAdd.children[index].ids.idGanancia.text) + float(totalMoney)

            except AttributeError:
                
                #Compra
                if self_page.ids.idCompra.text == '':
                    buyProducts = 0
                else:
                    buyProducts = float(self_page.ids.idCompra.text)

                #Ganancia
                if self_page.ids.idGanancia.text == '':
                    profitProducts = 0
                else:
                    profitProducts = float(self_page.ids.idGanancia.text)

                #Cantidad
                if self_page.ids.idCantidad.text == '':
                    amountProducts = 0
                else:
                    amountProducts = float(self_page.ids.idCantidad.text)

            
            totalProfitMoney = totalProfitMoney + (amountProducts * profitProducts)
            totalBuyMoney = totalBuyMoney + (amountProducts * buyProducts)
            

        totalMoney = float(totalProfitMoney) - float(totalBuyMoney)
        #totalMoney = amountProducts * profitProducts

        totalMoney = f"{totalMoney:.3f}"
        totalProfitMoney = f"{totalProfitMoney:.3f}"
        totalBuyMoney = f"{totalBuyMoney:.3f}"


        #Ganancia
        self_page.ids.moneyItemToSell.text = str(totalProfitMoney) + '$'

        #Compra
        self_page.ids.moneyItemBuy.text = str(totalBuyMoney) + '$'
        
        #Total
        self_page.ids.totalMoney.text = str(totalMoney) + '$'

        #moneyItemBuy = self_page.ids.moneyItemBuy.text.rstrip("$")
        #moneyItemToSell = self_page.ids.moneyItemToSell.text.rstrip("$")

        #total = float(moneyItemToSell) - float(moneyItemBuy)

        #Permite que solo se visualicen los primeros 3 digitos despues del punto
        #total = f"{total:.3f}"

    
    def SubmitData(self):

        name_product = []
        amount_product = []
        buy_product = []
        profit_product = []
        new_product = []

        #Dinero que se ganará/gastó/total
        money_buys = self.ids.moneyItemBuy.text
        money_profit = self.ids.moneyItemToSell.text
        money_total = self.ids.totalMoney.text

        #Nombre del proveedor
        name_supplier = self.ids.searchingSupplier.text
        #ID del proveedor
        id_supplier = self.ids.searchingSupplier.name
        
        for index, i in enumerate(self_page.ids.BoxLayoutChargeAdd.children):

            try:

                #Nuevo producto
                new_product.append(self.ids.BoxLayoutChargeAdd.children[index].ids.idProducto.verificationProduct)

                #Producto
                name_product.append(self.ids.BoxLayoutChargeAdd.children[index].ids.idProducto.text)
                #Cantidad
                amount_product.append(self.ids.BoxLayoutChargeAdd.children[index].ids.idCantidad.text)
                #Compra
                buy_product.append(self.ids.BoxLayoutChargeAdd.children[index].ids.idCompra.text)
                #Ganancia
                profit_product.append(self.ids.BoxLayoutChargeAdd.children[index].ids.idGanancia.text)

            except AttributeError:

                
                #Nuevo producto
                new_product.append(self.ids.idProducto.verificationProduct)

                #Producto
                name_product.append(self.ids.idProducto.text)
                #Cantidad
                amount_product.append(self.ids.idCantidad.text)
                #Compra
                buy_product.append(self.ids.idCompra.text)
                #Ganancia
                profit_product.append(self.ids.idGanancia.text)

        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(ChargesDB.InsertNewCharge, new_product, name_product, amount_product, buy_product, profit_product, name_supplier, id_supplier, money_buys, money_profit, money_total)
            return_value = future.result()
        
        if return_value == True:
            

            from MVC.controller.charges.charges_controller import self_charge_page
            from MVC.controller.store.store_controller import self_store_page

            from templates.table.table import ModalsDialog

            objecto = self_charge_page.ids.tableCharge.objecto
            objectoRv = self_charge_page.ids.tableCharge.objecto.rv

            objectoStore = self_store_page.ids.tableAlmacen.objecto
            objectoStoreRv = self_store_page.ids.tableAlmacen.objecto.rv

            #el primero es el objecto (variable objecto que lleva el widget weak), el segundo es el objecto.rv del recycleview
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                #Actualiza de la tabla Encargos/Compra
                executor.submit(ModalsDialog.ActualizeData, objecto, objectoRv)
                #Actualiza de la tabla Encargos/Compra
                executor.submit(ModalsDialog.ActualizeData, objectoStore, objectoStoreRv)

            toast('¡Compra agregada con éxito!')            
            functions.FunctionsKivys.ChangePage('self', 'ChargePage','Encargo')

        else:
            toast('Hubo un error' + str( return_value ))

        
