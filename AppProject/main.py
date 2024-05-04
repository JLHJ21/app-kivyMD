

#from kivymd.uix.screen import Screen

#Carga la variable KV, que contiene informacion .kv
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
import os

#Permite abrir la aplicación
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineAvatarIconListItem

from kivymd.uix.datatables import MDDataTable
from kivymd.uix.anchorlayout import MDAnchorLayout

from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

from kivymd.uix.pickers import MDDatePicker


#Permite pasar a otras paginas o ventas
from kivymd.uix.scrollview import MDScrollView

#Acomoda la resolución de la ventada, OJO solo para uso de desarrollo
from kivy.core.window import Window


#Enlazar archivo templates/table/table.py
import intermediary
from templates.table.table import RecycleViewTable, ModalsDialog

import weakref

#Window.size = (600, 800)

#OJO
#root.nav_drawer.set_state("close")
#IBA EN 
#DrawerClickableItem           

#VARIABLE QUE ALMACENA EL SELF, PERMITE CAMBIAR DE SCREN (PANTALLA) AUN SI SON DIFERENTES CLASES
intermediary.global_variable_self = global_self_client = ''
self_store_page = self_ClientsPage = self_sales_history = self_SupplierCharge = self_charge_page = self_money_history = None

#MENU LATERAL
class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


#CABECERA Y PIE DE PAGINA DE LA PAGINA
class HeaderAndFooter(MDScreen):
    pass


#PAGINA DE REGISTRAR CUENTA
class SignOn(MDScreen):
    def ChangePageToSignIn(self):
        
        #obtiene el self principal del kivy
        self_main = intermediary.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'SignIn'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Iniciar Sesión'
    pass

#PAGINA DE INICIO
class InitialPage(MDScreen):

    
    pass

#Pagina de cajero
class CashierPage(MDScreen):

    dialogShowUpdate = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_cashier_page
        self_cashier_page = self

    def CallbackMenuCashierPaymentType(self, button):

        intermediary.global_variable_self.MenuCashierPaymentType.caller = button
        intermediary.global_variable_self.MenuCashierPaymentType.open()

    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def CashierPaymentType(self = None, instance = ""):
        
        self_cashier_page.ids.ButtonMenuCashierPaymentType.text = instance
        intermediary.global_variable_self.MenuCashierPaymentType.dismiss()

#PAGINA DE DIVISAS

class ForeignExchangePage(MDScreen):

    inputDollar = StringProperty(None)
    inputPeso = StringProperty(None)
    inputBolivar = StringProperty(None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ChangeForeignExchange("dolar")



    def ChangeForeignExchange(self, text):

        match (text):
            case 'bolivar':

                dolar = 'Dolar a Bolívar: 1$ == 36.00bs'
                peso = 'Pesos a bolivares: 1000$$ == 10.5bs'
                bolivar = 'PREFERIDO'

            case 'dolar':
                dolar = 'PREFERIDO'
                peso = 'Pesos a dólares: 1000$$ == 0.25$'
                bolivar = 'Bolívar a dólar: 36.00bs == 1$'

            case 'peso':
                dolar = 'Dólar a pesos: 1$ == 3964$$'
                peso = 'PREFERIDO'
                bolivar = 'Bólivar a peso: 10.5bs == 1000$$'

            case _:
                dolar = 'Dolar a Bolívar: 1$ == 36.00bs'
                peso = 'Pesos a bolivares: 1000$$ == 10.5bs'
                bolivar = 'PREFERIDO'


        self.inputDollar = dolar
        self.inputPeso = peso
        self.inputBolivar = bolivar


#PAGINA DE INICIAR SESION
class SignIn(MDScreen):


    def ChangePageToSignOn(self):
        
        #obtiene el self principal del kivy
        self_main = intermediary.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'SignOn'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Registrarse'

    def OpenSystem(self, page):
        
        
        #obtiene el self principal del kivy
        self_main = intermediary.global_variable_self
        #cambia segun la pagina querida
        #print(self.parent)
        #print( self_main.root.ids.screen_manager.children )
        self_main.root.ids.screen_manager.current = 'InitialPage'

        #self_main.root.ids.screen_manager.current = 'headerandfooter'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        #self_main.root.ids.toolbar.title = text


    pass

        

#PAGINA DE PRESTAMOS
class LoanPage(MDScreen):


    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        Clock.schedule_once(lambda dt: self.ChangeItemsGrid('mes'))

    def ChangePageLoanPage(self):

        #obtiene el self principal del kivy
        self_main = intermediary.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'LoanAddPage'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Prestamo - Agregar'

    def ChangeItemsGrid(self, typeLoan):


        self.ids.gridLayoutLoanItems.clear_widgets()


        match typeLoan:
            case 'total':
                self.ids.buttonChangeTypeMoneyHistory.text = "Cambiar a: MES"
                self.ids.MoneyHistoryTitle.text = 'TOTAL'
                textAmountMoney = 'total XXX'
                pass
            case 'mes':
                self.ids.buttonChangeTypeMoneyHistory.text = "Cambiar a: TOTAL"
                self.ids.MoneyHistoryTitle.text = 'MES'

                textAmountMoney = 'mes XXX'
                pass
            case _:
                self.ids.buttonChangeTypeMoneyHistory.text = "Cambiar a: TOTAL"
                self.ids.MoneyHistoryTitle.text = 'TOTAL'

                textAmountMoney = 'total XXX'
            
                pass

        for i in range(0, 5):
        
            NewGridLayout = MDGridLayout(
                cols= 2,
                spacing= dp(20),
                padding= [dp(16), dp(18)],

                size_hint_y= None,
                height= dp(40)
            )

            NewLabels1 = MDLabel(
                        size_hint_x= 0.4,
                        text= "Ventas",
                        halign= "left",
                        font_style= "H6",
                    )
            

            NewLabels2 = MDLabel(

                    size_hint_x= 0.4,
                    halign= "right",

                    text= textAmountMoney,
                    mode= "rectangle",
                )



            NewGridLayout.add_widget(NewLabels1)
            NewGridLayout.add_widget(NewLabels2)

            self.ids.gridLayoutLoanItems.add_widget(NewGridLayout)


        NewLabels3 = MDLabel(
                        size_hint_x= 0.4,
                    )
            

        NewLabels4 = MDLabel(
                padding= [ dp(1), dp(40), dp(1), dp(1)],

                size_hint_x= 0.4,
                halign= "right",

                text= textAmountMoney,
                mode= "rectangle",
                underline= True,

            )
        

        NewGridLayout.add_widget(NewLabels3)
        NewGridLayout.add_widget(NewLabels4)

        #self.ids.gridLayoutLoanItems.add_widget(NewGridLayout)

       # self.ids.gridLayoutLoanItems
        
        
        pass


class LoanUpdatePage(MDScreen):
    pass

class LoanAddPage(MDScreen):

    pass

    

#PAGINA DE HISTORIAL DE DINERO/DIVISAS
class MoneyHistory(MDScreen):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_money_history
        self_money_history = self

    
    def ChangeTypeHistoryMoney(self):

        textTitle = self_money_history.ids.MoneyHistoryTitle.text

        match textTitle:
            case 'MES':
                variableTitle = 'TOTAL'
                variableLabelSales = '100'
                variableLabelCharge = '-60'
                variableTotalMoney = '40'
                variableChangeTypeMoneyHistory = 'Cambiar a: MES'

            case 'TOTAL':

                variableTitle = 'MES'
                variableLabelSales = '1000'
                variableLabelCharge = '-600'
                variableTotalMoney = '400'
                variableChangeTypeMoneyHistory = 'Cambiar a: TOTAL'
            case _:
                pass



        self_money_history.ids.MoneyHistoryTitle.text = variableTitle

        self_money_history.ids.LabelSalesProducts.text = variableLabelSales

        self_money_history.ids.LabelChargeProducts.text = variableLabelCharge

        self_money_history.ids.LabelTotalMoney.text = variableTotalMoney

        self_money_history.ids.buttonChangeTypeMoneyHistory.text = variableChangeTypeMoneyHistory




class ScrollViewWidget(MDScrollView):
    pass

    
#PAGINA DE HISTORIAL DE VENTAS
class SalesHistoryPage(MDScreen):

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_sales_history
        self_sales_history = self


    def CallbackMenuSalesHistory(self, button):

        MenuAndTitleSelect.DropMenu("self", button, intermediary.global_variable_self.MenuTypeSalesHistory)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeSalesHistory(self, Text):


        MenuAndTitleSelect.ChangeNameDropMenu(self_sales_history, intermediary.global_variable_self.MenuTypeSalesHistory, "ButtonMenuSearchingSalesHistory", Text)

        
        
#PAGINA DE CONFIGURACION
class ContentConfigurationPage(MDBoxLayout):



    inputOne= StringProperty(None)
    inputTwo= StringProperty(None)

    
    def Variables(nameInputOne, nameInputTwo):
        ContentConfigurationPage.inputOne = nameInputOne
        ContentConfigurationPage.inputTwo = nameInputTwo


        #print(ContentConfigurationPage.inputOne )


class ConfigurationPage(MDScreen):

    dialogUsername = dialogPassword = dialogEmail = None

    def OpenModal(self, inputOneName, inputTwoName, dialogName, title):
        ContentConfigurationPage.Variables(inputOneName, inputTwoName)

        match dialogName:
            case 'dialogUsername':
                self_name = self.dialogUsername
            
            case 'dialogEmail':
                self_name = self.dialogEmail
            
            case 'dialogPassword':
                self_name = self.dialogPassword

            case _:
                self_name = self.dialogUsername


        if not self_name:
            self_name = MDDialog(
                title=title,
                type="custom",
                content_cls=ContentConfigurationPage(),
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        md_bg_color="red",
                        text_color="white",
                    ),
                    MDRaisedButton(
                        text="Aceptar",
                        md_bg_color="blue",
                        #text_color=self.theme_cls.primary_color,
                    ),
                ],
            )
        self_name.open()


#PAGINA DE ALMACEN
class StorePage(MDScreen):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_store_page
        self_store_page = self

    def CallbackMenuProduct(self, button):

        MenuAndTitleSelect.DropMenu("self", button, intermediary.global_variable_self.MenuProductoTypeStore)

        #intermediary.global_variable_self.MenuProductoTypeStore.caller = button
        #intermediary.global_variable_self.MenuProductoTypeStore.open()


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeStore(self, Text):

        #print(self_store_page.ids)
        #print(instance)


        MenuAndTitleSelect.ChangeNameDropMenu(self_store_page, intermediary.global_variable_self.MenuProductoTypeStore, "ButtonMenuSearchingStore", Text)
        
        #self_store_page.ids.ButtonMenuSearchingStore.text = instance
        #intermediary.global_variable_self.MenuProductoTypeStore.dismiss()

    
class StoreUpdatePage(MDScreen):
    
    pass


#Clase para la seleccion de fotos, pagina
class ChooseImagePage(MDScreen):

    global_root = ""

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        Window.bind(on_keyboard=self.events)
        #self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, 
            select_path=self.select_path,
            preview=True,
            icon_selection_button="pencil",
        )
    
    #Abre el seleccionador
    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        #self.manager_open = True

    #Archivo seleccionado
    def select_path(self, path: str):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''

        #Cambia el source de la imagen
        self.manager.get_screen("StorePageUpdate").ids.imageProduct.source = path

        #Cambia la pagina
        self.manager.current = 'StorePageUpdate'

        #global_root.manager.screen_manager.current = "StorePageUpdate"
        self.exit_manager()
        #toast(path)

    #Permite cerrar el seleccionador
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        #self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


class MenuAndTitleSelect():

    def DropMenu(self, button, DropMenu):

        DropMenu.caller = button
        DropMenu.open()


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeNameDropMenu(self, DropMenu, IdButton, Text = ""):
        
        self.ids[IdButton].text = Text
        DropMenu.dismiss()

#PAGINA DEL CLIENTE
class ClientsPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_ClientsPage
        self_ClientsPage = self


    def CallbackMenuClients(self, button):

        MenuAndTitleSelect.DropMenu("self", button, intermediary.global_variable_self.MenuTypeClientsPage)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeClients(self = None, Text = ""):
        MenuAndTitleSelect.ChangeNameDropMenu(self_ClientsPage, intermediary.global_variable_self.MenuTypeClientsPage, "ButtonMenuSearchingClient", Text)


class ChargePage(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_charge_page
        self_charge_page = self

    def CallbackMenuCharge(self, button):


        MenuAndTitleSelect.DropMenu("self", button, intermediary.global_variable_self.MenuTypeChargePage)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeCharge(self = None, Text = ""):

        MenuAndTitleSelect.ChangeNameDropMenu(self_charge_page, intermediary.global_variable_self.MenuTypeChargePage, "ButtonMenuSearchingCharge", Text)


#PAGINA DE PROVEEDOR
class SupplierPage(MDScreen):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_SupplierCharge
        self_SupplierCharge = self

    
    def ChangePageSupplierPage(self):

        #obtiene el self principal del kivy
        self_main = intermediary.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'SupplierAddPage'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Proveedor - Agregar'
    

    def CallbackMenuSupplier(self, button):

        MenuAndTitleSelect.DropMenu("self", button, intermediary.global_variable_self.MenuTypeSupplierPage)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeSupplier(self = None, Text = ""):

        MenuAndTitleSelect.ChangeNameDropMenu(self_SupplierCharge, intermediary.global_variable_self.MenuTypeSupplierPage, 'ButtonMenuSearchingSupplier', Text)

class SupplierUpdatePage(MDScreen):
    pass

class SupplierAddPage(MDScreen):
    pass

#CLASE DE DATEPICKER
class DatePicker():

    datePicker = None

    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''

        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):

        if not self.datePicker:
            self.datePicker =  MDDatePicker(mode="range")
            self.datePicker.bind(on_save=self.on_save, on_cancel=self.on_cancel)

        self.datePicker.open()

#CLASE DE LA APLICACION
class App(MDApp):

    modals = ModalsDialog()
    datePicker = DatePicker()

    #LO PRIMERO QUE SE CARGA
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #Crea la variable global, self de la aplicación para poder ser utilizada en otras clases y archivos .py
        intermediary.GlobalVariables.GetGlobalSelf(self)


        #CARGA LOS DATOS DE .KV
        self.screen = Builder.load_file("styles.kv")

        #PROCESO QUE ALMACENA DE FORMA GLOBAL LOS DATOS DE SELF EN GLOBAL_SELF

        ##  MENU 1RA MANERA, PARA SOLO MDTopAppBar
        #TASA DE MONEDA
        menu_foreign_exchange_header = [
            
            {
                "text": "Dolar",
                "leading_icon": "cash-100",
                "on_press": lambda x='Item Dolar': self.CallbackTypeMoney('dolar'),
            },
            {
                "text": "Peso",
                "leading_icon": "cash-fast",
                "on_press": lambda x='Item Peso': self.CallbackTypeMoney('peso'),
            },
            {
                "text": "Bolívar",
                "leading_icon": "cash-off",
                "on_press": lambda x='Item Bolivar': self.CallbackTypeMoney('bolivar'),
            }
        ]
        self.menu = MDDropdownMenu(
            border_margin=dp(4),
            items=menu_foreign_exchange_header,
            width=dp(240),
            hor_growth="left",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )

    
        #PERFIL DE USUARIO
        menu_configuration_header = [
            {
                "text": "Configuración",
                "leading_icon": "account-settings",
                "on_press": lambda x='Item configuracion': self.callback(x),
            },
            {
                "text": "Cerrar Sesión",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='Item perfil': self.callback(x),
            },
        ]
        self.menu2 = MDDropdownMenu(
            border_margin=dp(4),
            items=menu_configuration_header,
            width=dp(240),
            hor_growth="left",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )

        ##  MENU 2RA MANERA, PARA SOLO MDBUTTON
        #Menu almacen 


        menu_store = [
            
            {
                "text": "TODO",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='TODO': StorePage.ChangeSearchingTypeStore("",x),
            },
            {
                "text": "CANTIDAD ASC",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='CANTIDAD ASC': StorePage.ChangeSearchingTypeStore("",x),
            },
            {
                "text": "CANTIDAD DES",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='CANTIDAD DES': StorePage.ChangeSearchingTypeStore("",x),
            },
            {
                "text": "PRECIO ASC",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='PRECIO ASC': StorePage.ChangeSearchingTypeStore("",x),
            },
            {
                "text": "PRECIO DES",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='PRECIO DES': StorePage.ChangeSearchingTypeStore("",x),
            },
        ]
        
        self.MenuProductoTypeStore = MDDropdownMenu(
            #caller=self.screen.ids.ButtonMenuSearchingStore,
            border_margin=dp(4),
            items=menu_store,
            hor_growth="right",
            ver_growth="down",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )

        menu_foreign_exchange = [
            {
                "text": "Dolar",
                "leading_icon": "cash-100",
                "on_press": lambda x='Item Dolar': CashierPage.CashierPaymentType(x, 'Dólar'),
            },
            {
                "text": "Peso",
                "leading_icon": "cash-fast",
                "on_press": lambda x='Item Peso': CashierPage.CashierPaymentType(x, 'Peso'),
            },
            {
                "text": "Bolívar",
                "leading_icon": "cash-off",
                "on_press": lambda x='Item Bolivar': CashierPage.CashierPaymentType(x, 'Bolívar'),
            }
        ]

        self.MenuCashierPaymentType = MDDropdownMenu(
            #caller=self.screen.ids.ButtonMenuSearchingStore,
            border_margin=dp(4),
            items=menu_foreign_exchange,
            #hor_growth="center",
            ver_growth="down",
            position="bottom",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )


        menu_sale_history = [

            {
                "text": "TODO",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='TODO': SalesHistoryPage.ChangeSearchingTypeSalesHistory("",x),
            },
            {
                "text": "CLIENTE",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='CLIENTE': SalesHistoryPage.ChangeSearchingTypeSalesHistory("",x),
            },
            {
                "text": "EMPLEADO",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='EMPLEADO': SalesHistoryPage.ChangeSearchingTypeSalesHistory("",x),
            },
            {
                "text": "FECHA ASC",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='FECHA ASC': SalesHistoryPage.ChangeSearchingTypeSalesHistory("",x),
            },
            {
                "text": "FECHA DESC",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='FECHA DESC': SalesHistoryPage.ChangeSearchingTypeSalesHistory("",x),
            },
        ]

        self.MenuTypeSalesHistory = MDDropdownMenu(

            border_margin=dp(4),
            items=menu_sale_history,
            #hor_growth="center",
            ver_growth="down",
            position="bottom",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )


        menu_clients = [

            {
                "text": "TODO",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='TODO': ClientsPage.ChangeSearchingTypeClients("",x),
            },
            {
                "text": "DADO POR",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='DADO POR': ClientsPage.ChangeSearchingTypeClients("",x),
            },
            {
                "text": "FECHA ASC",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='FECHA ASC': ClientsPage.ChangeSearchingTypeClients("",x),
            },
            {
                "text": "FECHA DESC",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='FECHA DESC': ClientsPage.ChangeSearchingTypeClients("",x),
            },
        ]

        self.MenuTypeClientsPage = MDDropdownMenu(

            border_margin=dp(4),
            items=menu_clients,
            #hor_growth="center",
            ver_growth="down",
            position="bottom",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )

        menu_supplier = [

            {
                "text": "TODO",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='TODO': SupplierPage.ChangeSearchingTypeSupplier("",x),
            },
            {
                "text": "NOMBRE",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='NOMBRE': SupplierPage.ChangeSearchingTypeSupplier("",x),
            },
            {
                "text": "UBICACION",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='UBICACION': SupplierPage.ChangeSearchingTypeSupplier("",x),
            },
            {
                "text": "RIF",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='RIF': SupplierPage.ChangeSearchingTypeSupplier("",x),
            },
            {
                "text": "TELÉFONO",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='TELÉFONO': SupplierPage.ChangeSearchingTypeSupplier("",x),
            },
        ]

        self.MenuTypeSupplierPage = MDDropdownMenu(

            border_margin=dp(4),
            items=menu_supplier,
            #hor_growth="center",
            ver_growth="down",
            position="bottom",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )

        menu_charge = [

            {
                "text": "TODO",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='TODO': ChargePage.ChangeSearchingTypeCharge("",x),
            },
            {
                "text": "ID",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='ID': ChargePage.ChangeSearchingTypeCharge("",x),
            },
            {
                "text": "PROVEEDOR",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='PROVEEDOR': ChargePage.ChangeSearchingTypeCharge("",x),
            },
            {
                "text": "CANTIDAD",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='CANTIDAD': ChargePage.ChangeSearchingTypeCharge("",x),
            },
            {
                "text": "GASTO",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='GASTO': ChargePage.ChangeSearchingTypeCharge("",x),
            },
        ]

        self.MenuTypeChargePage = MDDropdownMenu(

            border_margin=dp(4),
            items=menu_charge,
            #hor_growth="center",
            ver_growth="down",
            position="bottom",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )

    def build(self):

        self.title = 'App'
        #self.theme_cls.primary_palette = "Orange"
        #self.theme_cls.theme_style = "Dark"
        return self.screen

    def callback(self, instance_action_top_appbar_button):
        print(instance_action_top_appbar_button)

    ## CALLBACK DE MDTopAppBar
    def CallbackModeScreen(self, instance_action_top_appbar_button, action = None):

        match action:
            case 'claro':
                items = [
                        ["weather-sunny", lambda x: self.CallbackModeScreen(x, 'oscuro'), "Modo Claro", "Modo Claro"],
                    ]
            case 'oscuro':
                items = [
                        ["moon-waning-crescent", lambda x: self.CallbackModeScreen(x, 'claro'), "Modo Oscuro", "Modo Oscuro"],
                    ]
            case _:
                items = [
                        ["weather-sunny", lambda x: self.CallbackModeScreen(x, 'oscuro'), "Modo Claro", "Modo Claro"],
                    ]

        itemsIcons = items
        
        self.root.ids.toolbar.right_action_items[1] = itemsIcons[0]

    def CallbackTypeMoney(self, action = None):

        match action:
            case 'dolar':
                items = [
                        ["cash-100", lambda x: self.CallbackMenuChangeMoney(x), "Tipo de tasa - Dolar", "Tipo de tasa - Dolar"],
                    ]
            case 'peso':
                items = [
                        ["cash-fast", lambda x: self.CallbackMenuChangeMoney(x), "Tipo de tasa - Pesos", "Tipo de tasa - Pesos"],
                    ]
            case 'bolivar':
                items = [
                        ["cash-off", lambda x: self.CallbackMenuChangeMoney(x), "Tipo de tasa - Bolívar", "Tipo de tasa - Bolívar"],
                    ]
            case _:
                items = [
                        ["cash-100", lambda x: self.CallbackMenuChangeMoney(x), "Tipo de tasa - Dolar", "Tipo de tasa - Dolar"],
                    ]
        
        self.root.ids.toolbar.right_action_items[0] = items[0]
        self.menu.dismiss()

    def CallbackMenuChangeMoney(self, button):
        
        self.menu.caller = button
        self.menu.open()

    def CallbackMenuUser(self, button):
        
        self.menu2.caller = button
        self.menu2.open()

    ## CALLBACK PARA CAMBIAR DE PAGINA CON MDTopAppBar BUTTON
    '''
    def ChangePage(self, page, text, dontSelf = None, extra = None):


        if dontSelf == None:
            self.root.ids.screen_manager.current = page
            self.root.ids.toolbar.title = text

            global intermediary.global_variable_self
            intermediary.global_variable_self = intermediary.GlobalVariables.GetGlobalSelf(self)
            

        elif dontSelf == True:

            match page:
                case 'StorePageUpdate':
                    ClientsTable.CloseDialogStorePage(extra, 'obj')
                case _:
                    pass

            intermediary.global_variable_self.root.ids.screen_manager.current = page
            intermediary.global_variable_self.root.ids.toolbar.title = text
    '''

    def ShowImage(self, path):
        intermediary.global_variable_self.root.ids.imageProduct.source = path


## CLASE PARA MOSTRAR LA TABLA, MDDATATABLE
'''
class ClientsTable(MDBoxLayout):

    dialog = None
    dialog2 = None
    dialog3 = None

    def ShowAlertDialog(self):

        #global global_self_client
        #global_self_client = self

        print(self)
        """
        if not self.dialog:
            self.dialog = MDDialog(
                title="¿Que desea realizar?",
                text="Por favor, elija algunas de las opciones presentadas.",
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        #text_color=self.theme_cls.primary_color,
                        on_release = self.CloseDialogStorePage
                    ),
                    MDRaisedButton(
                        text="Eliminar",
                        md_bg_color="red",
                        text_color="white",
                        on_release = self.ShowAlertDialogDelete

                    ),
                    MDRaisedButton(
                        text="Modificar",
                        md_bg_color="orange",
                        on_release= lambda x: App.ChangePage(x,"StorePageUpdate", "Almacen - Modificar", True, self)
                                                        
                    ),
                ],
            )
        self.dialog.open()
        """
    def ShowAlertDialogDelete(self, obj):

        self.CloseDialogStorePage('obj')

        if not self.dialog2:
            self.dialog2 = MDDialog(
                title="¿De verdad quiere eliminar este producto?",
                text="Si es así, adelante",
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        text_color= "red",
                        on_release = self.CloseDialogDelete
                    ),
                    MDRaisedButton(
                        text="Eliminar",
                        text_color="white",
                        md_bg_color="red",
                        on_release = self.DeleteProduct
                    ),
                ],
            )
        self.dialog2.open()

    def DeleteProduct(self, obj):

        self.CloseDialogDelete('obj')

        if not self.dialog3:
            self.dialog3 = MDDialog(
                title="¡Se ha realizado con éxito!",
                text="Se ha eliminado el producto sin ningún inconveniente.",
                buttons=[
                    MDRaisedButton(
                        text="Ok",
                        on_release = self.CloseDialogDeleteConfirmation
                    ),
                ],
            )
        self.dialog3.open()

    def CloseDialogStorePage(self, obj):
        self.dialog.dismiss()

    def CloseDialogDelete(self, obj):
        self.dialog2.dismiss()

    def CloseDialogDeleteConfirmation(self, obj):
        self.dialog3.dismiss()

    #def on_enter(self):
    #    print('entro en on_enter')
    #    self.load_table()

'''
## TABLA

## CLASE PARA MOSTRAR LA TABLA, MDDATATABLE
class CashierTableProductsToOffer(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #print('entro en load_table')
        layout = MDAnchorLayout()


        self.data_tables = MDDataTable(
            pos_hint={'center_y': 1, 'center_x': 1},
            size_hint=(1, 1),
            padding= [dp(16), dp(1), dp(16), dp(1)],
            use_pagination=True,
            column_data=[
                ("Imagen", dp(25)),
                ("Nombre", dp(25)),
                ("Cantidad", dp(20)),
            ],
            row_data=[
                (
                    "imagen.jpg",
                    "Harina",
                    "42"
                )
                for i in range(50)],)
        
        self.data_tables.bind(on_row_press=self.on_row_press)
        layout.add_widget(self.data_tables)
        self.add_widget(layout)
        #return layout

    def on_row_press(self, instance_table, instance_row):
        print(instance_table, instance_row)

class CashierTableProductsToSell(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #print('entro en load_table')
        layout = MDAnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 1, 'center_x': 1},
            size_hint=(1, 1),
            padding= [dp(16), dp(32), dp(16), dp(1)],
            use_pagination=True,
            column_data=[
                ("Imagen", dp(30)),
                ("Nombre", dp(30)),
                ("Proveedor", dp(30)),
                ("Cantidad", dp(30)),
                ("Precio", dp(15))
            ],
            row_data=[
                (
                    "imagen.jpg",
                    "Arroz",
                    "Polar S.A.",
                    "42",
                    "62.5",
                )
                for i in range(10)],)
        
        self.data_tables.bind(on_row_press=self.on_row_press)
        layout.add_widget(self.data_tables)
        self.add_widget(layout)
        #return layout

    def on_row_press(self, instance_table, instance_row):
        print(instance_table, instance_row)

App().run()