

#from kivymd.uix.screen import Screen

#Carga la variable KV, que contiene informacion .kv
from kivy.lang import Builder
from kivy.metrics import dp
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


#Permite pasar a otras paginas o ventas
from kivymd.uix.scrollview import MDScrollView

#Acomoda la resolución de la ventada, OJO solo para uso de desarrollo
from kivy.core.window import Window


#Enlazar archivo templates/table/table.py
import intermediary
from templates.table.table import RecycleViewTable


#Window.size = (600, 800)

#OJO
#root.nav_drawer.set_state("close")
#IBA EN 
#DrawerClickableItem           

#VARIABLE QUE ALMACENA EL SELF, PERMITE CAMBIAR DE SCREN (PANTALLA) AUN SI SON DIFERENTES CLASES
global_self = global_self_client = ''
self_store_page = None

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class HeaderAndFooter(MDScreen):
    pass

class InitialPage(MDScreen):
    pass

class CashierPage(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_cashier_page
        self_cashier_page = self

    def CallbackMenuCashierPaymentType(self, button):

        global_self.MenuCashierPaymentType.caller = button
        global_self.MenuCashierPaymentType.open()

    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def CashierPaymentType(self = None, instance = ""):
        
        self_cashier_page.ids.ButtonMenuCashierPaymentType.text = instance
        global_self.MenuCashierPaymentType.dismiss()

    pass

class StoreUpdatePage(MDScreen):
    
    pass


class StorePage(MDScreen):
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_store_page
        self_store_page = self

    def CallbackMenuProduct(self, button):

        global_self.MenuProductoTypeStore.caller = button
        global_self.MenuProductoTypeStore.open()


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeStore(self = None, instance = ""):
        
        self_store_page.ids.ButtonMenuSearchingStore.text = instance
        global_self.MenuProductoTypeStore.dismiss()

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
class App(MDApp):

    #LO PRIMERO QUE SE CARGA
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #CARGA LOS DATOS DE .KV
        self.screen = Builder.load_file("styles.kv")

        #PROCESO QUE ALMACENA DE FORMA GLOBAL LOS DATOS DE SELF EN GLOBAL_SELF
        global global_self
        global_self = intermediary.GlobalVariables.GetGlobalSelf(self)

        ##  MENU 1RA MANERA, PARA SOLO MDTopAppBar
        #TASA DE MONEDA
        menu_items = [
            
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
            items=menu_items,
            width=dp(240),
            hor_growth="left",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )

    
        #PERFIL DE USUARIO
        menu_items2 = [
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
            items=menu_items2,
            width=dp(240),
            hor_growth="left",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )

        ##  MENU 2RA MANERA, PARA SOLO MDBUTTON
        #Menu almacen 


        menu_items3 = [
            
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
            items=menu_items3,
            hor_growth="right",
            ver_growth="down",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )

        menu_items4 = [
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
            items=menu_items4,
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

            global global_self
            global_self = intermediary.GlobalVariables.GetGlobalSelf(self)
            

        elif dontSelf == True:

            match page:
                case 'StorePageUpdate':
                    ClientsTable.CloseDialogStorePage(extra, 'obj')
                case _:
                    pass

            global_self.root.ids.screen_manager.current = page
            global_self.root.ids.toolbar.title = text
    '''

    def ShowImage(self, path):
        global_self.root.ids.imageProduct.source = path


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