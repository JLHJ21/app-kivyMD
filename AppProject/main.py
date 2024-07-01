#####KIVY LIBRERIAS
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
#Acomoda la resolución de la ventada, OJO solo para uso de desarrollo
from kivy.core.window import Window

#####KIVYMD LIBRERIAS

#Permite abrir la aplicación
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.scrollview import MDScrollView

#####FUNCIONES PYTHON
import os
from functools import partial
import weakref
from passlib.hash import sha256_crypt


#####ENLAZAR ARCHIVOS PYTHON/KIVY

#Enlazar archivo templates/table/table.py
from templates.table.table import ModalsDialog , RecycleViewTable

#Enlazar página de inicio "InitialPage" MVC/controller/home/home_controller.py 
from MVC.controller.home.home_controller import InitialPage

#Enlazar página de inicio "CashierPage" MVC/controller/cashier/cashier_controller.py 
from MVC.controller.cashier.cashier_controller import CashierPage

#Enlazar página de inicio "StorePage" MVC/controller/store/store_controller.py 
from MVC.controller.store.store_controller import StorePage

#Enlazar página de inicio "StoreUpdatePage" MVC/controller/store/update/store_update_controller.py 
from MVC.controller.store.update.store_update_controller import StoreUpdatePage


#Enlazar página de inicio "chooseimagePage" MVC/controller/store/choose_image/choose_image_controller.py 
from MVC.controller.store.choose_image.choose_image_controller import ChooseImagePage


#Enlazar página de inicio "ClientsPage" MVC/controller/clients/clients_controller.py 
from MVC.controller.clients.clients_controller import ClientsPage

#Enlazar página "ClientAddPage" MVC/controller/clients/add/add_clients_controller.py 
from MVC.controller.clients.add.add_clients_controller import ClientAddPage

#Enlazar página "ClientUpdatePage" MVC/controller/clients/update/update_clients_controller.py 
from MVC.controller.clients.update.update_clients_controller import ClientUpdatePage


#Enlazar página de inicio "ConfigurationPage" MVC/controller/configuration/configuration_controller.py 
from MVC.controller.configuration.configuration_controller import ConfigurationPage

#Enlazar página de inicio "ForeignExchange" MVC/controller/foreign_exchange/foreign_exchange_controller.py 
from MVC.controller.foreign_exchange.foreign_exchange_controller import ForeignExchangePage

#Enlazar página de inicio "UpdateForeignExchange" MVC/controller/foreign_exchange/update/update_foreign_exchange.py 
from MVC.controller.foreign_exchange.update.update_foreign_exchange_controller import UpdateForeignExchangePage

#Enlazar página de inicio "UpdateForeignExchange" MVC/controller/foreign_exchange/update/update_foreign_exchange.py 
from MVC.controller.sales_history.sales_history_controller import SalesHistoryPage


#Enlazar página de inicio "SupplierPage" MVC/controller/supplier/supplier_controller.py 
from MVC.controller.supplier.supplier_controller import SupplierPage

#Enlazar página de inicio "SupplierPage" MVC/controller/supplier/update/update_supplier_controller.py 
from MVC.controller.supplier.update.update_supplier_controller import SupplierUpdatePage

#Enlazar página de inicio "SupplierPage" MVC/controller/supplier/add/add_supplier_controller.py 
from MVC.controller.supplier.add.add_supplier_controller import SupplierAddPage

#Enlazar página de inicio "ChargePage" MVC/controller/charges/charges_controller.py 
from MVC.controller.charges.charges_controller import ChargePage

#Enlazar página de inicio "ChargeAddPage" MVC/controller/charges/add/add_charges_controller.py 
from MVC.controller.charges.add.add_charges_controller import ChargeAddPage


#Enlazar página de inicio "ChargeChooseImagePage" MVC/controller/charges/choose_image_charges/choose_image_charges_controller.py 
from MVC.controller.charges.choose_image_charges.choose_image_charges_controller import ChargeChooseImagePage

#Enlazar página de inicio "MoneyHistoryPage" MVC/controller/money_history/money_history_controller.py 
from MVC.controller.money_history.money_history_controller import MoneyHistoryPage

#Enlazar página de inicio "LoanPage" MVC/controller/loans/loans_controller.py 
from MVC.controller.loans.loans_controller import LoanPage

#Enlazar página de inicio "LoanAddPage" MVC/controller/loans/add/add_loans_controller.py 
from MVC.controller.loans.add.add_loans_controller import LoanAddPage

#Enlazar página de inicio "LoanUpdatePage" MVC/controller/loans/update/update_loans_controller.py 
from MVC.controller.loans.update.update_loans_controller import LoanUpdatePage

#Enlazar página de inicio "SignIn" MVC/controller/sign_in/sign_in_controller.py 
from MVC.controller.sign_in.sign_in_controller import SignInPage

#Enlazar página de inicio "SignOn" MVC/controller/sign_on/sign_on_controller.py 
from MVC.controller.sign_on.sign_on_controller import SignOnPage

#Enlazar página de inicio "SignOn" MVC/controller/sign_on/sign_on_controller.py 
from MVC.controller.header_footer.header_footer_controller import HeaderAndFooter

#Enlazar archivo de base de datos
#Enlazar archivo de base de datos database/database.py
from database.database import DatabaseClass


#import intermediary
import MVC.controller.functions as functions
import concurrent.futures


#Window.size = ( 720, 1600 )

#OJO
#root.nav_drawer.set_state("close")
#IBA EN 
#DrawerClickableItem           

#VARIABLE QUE ALMACENA EL SELF, PERMITE CAMBIAR DE SCREN (PANTALLA) AUN SI SON DIFERENTES CLASES
#functions.global_variable_self =
global_self_client = ''
self_store_page = self_ClientsPage = self_sales_history = self_SupplierCharge = self_charge_page = self_money_history = global_foreign_exchange_update = None

#productos
#DatabaseClass.InsertData()

import cProfile

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

import threading
#CLASE DE LA APLICACION
class App(MDApp):


    #LO PRIMERO QUE SE CARGA
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        
        # LLAMADA A LA BASE DE DATOS
        #functions.executor.submit(DatabaseClass.Conexion)

        #Crea la variable global, self de la aplicación para poder ser utilizada en otras clases y archivos .py
        functions.GlobalVariables.GetGlobalSelf(self)
        #DatabaseClass.Conexion()

        #t1 = threading.Thread(target=DatabaseClass.Conexion())# Here is where I have tried to thread the function
        #t1.start()

        #CARGA LOS DATOS DE .KV
        self.screen = Builder.load_file("styles.kv")

        #self.table = RecycleViewTable()
        
        self.modals = ModalsDialog()
        self.datePicker = DatePicker()
        self.database = DatabaseClass()
        self.functions_callback = functions.FunctionsKivys()
        #self.table = RecycleViewTable()
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
                "text": "Dólar",
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

    

    ## CALLBACK PARA CAMBIAR DE PAGINA CON MDTopAppBar BUTTON
    '''
    def ChangePage(self, page, text, dontSelf = None, extra = None):


        if dontSelf == None:
            self.root.ids.screen_manager.current = page
            self.root.ids.toolbar.title = text

            global functions.global_variable_self
            functions.global_variable_self = functions.GlobalVariables.GetGlobalSelf(self)
            

        elif dontSelf == True:

            match page:
                case 'StorePageUpdate':
                    ClientsTable.CloseDialogStorePage(extra, 'obj')
                case _:
                    pass

            functions.global_variable_self.root.ids.screen_manager.current = page
            functions.global_variable_self.root.ids.toolbar.title = text
    '''

    def ShowImage(self, path):
        functions.global_variable_self.root.ids.imageProduct.source = path


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
'''
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
'''

App().run()