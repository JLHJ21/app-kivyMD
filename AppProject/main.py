

#from kivymd.uix.screen import Screen

#Carga la variable KV, que contiene informacion .kv
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty

#Permite abrir la aplicación
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen, ScreenManager

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineAvatarIconListItem

from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.anchorlayout import MDAnchorLayout

from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.widget import MDWidget
from kivymd.uix.boxlayout import MDBoxLayout


#Permite pasar a otras paginas o ventas
from kivymd.uix.scrollview import MDScrollView

#Acomoda la resolución de la ventada, OJO solo para uso de desarrollo
from kivy.core.window import Window
#Window.size = (600, 800)

#OJO
#root.nav_drawer.set_state("close")
#IBA EN 
#DrawerClickableItem           


KV = '''

<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: "#4a4939"
    icon_color: "#4a4939"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"


<DrawerLabelItem@MDNavigationDrawerItem>
    text_color: "#4a4939"
    icon_color: "#4a4939"
    focus_behavior: False
    selected_color: "#4a4939"
    _no_ripple_effect: True

<ContentNavigationDrawer>

    MDNavigationDrawerMenu:

        MDNavigationDrawerHeader:
            title: "BroxElt S.A."
            title_color: "#4a4939"
            text: "Bienvenido XXXXX"
            source: "logo.jpg"
            spacing: "4dp"
            padding: "12dp", 0, 0, "40dp"

        MDNavigationDrawerLabel:
            text: "General"

        MDNavigationDrawerDivider:
            padding: dp(10),0, dp(12), dp(1)

        DrawerClickableItem:
            icon: "home"
            text_right_color: "#4a4939"
            text: "Panel de control"

            on_press:
                root.screen_manager.current = "InitialPage"

                app.root.ids.toolbar.title = self.text

        DrawerClickableItem:
            icon: "cash-register"
            text_right_color: "#4a4939"
            text: "Cajero"

            on_press:
                root.screen_manager.current = "InitialPage"

                app.root.ids.toolbar.title = self.text

        DrawerClickableItem:
            icon: "store"
            text_right_color: "#4a4939"
            text: "Almacen"
            on_press:
                root.screen_manager.current = "StorePage"

                app.root.ids.toolbar.title = self.text
        
        DrawerClickableItem:
            icon: "cash-clock"
            text_right_color: "#4a4939"
            text: "Presupuesto"
            on_press:
                root.screen_manager.current = "scr 2"

                app.root.ids.toolbar.title = self.text
        
        DrawerClickableItem:
            icon: "account-cash"
            text_right_color: "#4a4939"
            text: "Cliente"
            on_press:
                root.screen_manager.current = "scr 2"

                app.root.ids.toolbar.title = self.text
        
                

        MDNavigationDrawerLabel:
            text: "Administrador"
            padding: dp(16), dp(10), dp(12), dp(10)


        MDNavigationDrawerDivider:
            padding: dp(10), 0, dp(12), dp(1)

        DrawerClickableItem:
            icon: "cube-send"
            text_right_color: "#4a4939"
            text: "Encargos"

            on_press:
                root.screen_manager.current = "InitialPage"

                app.root.ids.toolbar.title = self.text

        DrawerClickableItem:
            icon: "cash-multiple"
            text_right_color: "#4a4939"
            text: "Divisas"

            on_press:
                root.screen_manager.current = "InitialPage"

                app.root.ids.toolbar.title = self.text

        DrawerClickableItem:
            icon: "account-multiple"
            text_right_color: "#4a4939"
            text: "Proveedores"

            on_press:
                root.screen_manager.current = "InitialPage"

                app.root.ids.toolbar.title = self.text
        
        DrawerClickableItem:
            icon: "cash-remove"
            text_right_color: "#4a4939"
            text: "Prestamos"

            on_press:
                root.screen_manager.current = "InitialPage"

                app.root.ids.toolbar.title = self.text

        DrawerClickableItem:
            icon: "receipt-text-clock"
            text_right_color: "#4a4939"
            text: "Historial de Ventas"

            on_press:
                root.screen_manager.current = "InitialPage"

                app.root.ids.toolbar.title = self.text
        
        DrawerClickableItem:
            icon: "text-box-search"
            text_right_color: "#4a4939"
            text: "Historial de Dinero"

            on_press:
                root.screen_manager.current = "InitialPage"

                app.root.ids.toolbar.title = self.text


                
        MDNavigationDrawerLabel:
            text: "Configuraciones"
            padding: dp(16), dp(10), dp(12), dp(10)

        MDNavigationDrawerDivider:
            padding: dp(10), 0, dp(12), dp(1)

        DrawerClickableItem:
            icon: "account-cog"
            text_right_color: "#4a4939"
            text: "Configuracion"

            on_press:
                root.screen_manager.current = "InitialPage"

                app.root.ids.toolbar.title = self.text

MDScreen:

    MDTopAppBar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 4
        title: "MDNavigationDrawer"
        use_overflow: True
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
        right_action_items:
            [
            ["cash-100", lambda x: app.CallbackMenuChangeMoney(x), "Tipo de tasa - Dolar", "Tipo de tasa - Dolar"],
            ["weather-sunny", lambda x: app.CallbackModeScreen(x, 'oscuro'), "Modo Claro", "Modo Claro"],
            ["account-settings", lambda x: app.CallbackMenuUser(x), "Perfil" , "Perfil"],
            ]
            
    MDTopAppBar:
        id: toolbarbottom
        type_height: "small"
        headline_text: "Headline"
        title: "BroxElt S.A."
        elevation: 4
        anchor_title: "left"
        use_overflow: True
        
        right_action_items:
            [             
            ["account-cog", lambda x: app.callback(x), "", "Configuracion"],             
            ["cash-remove", lambda x: app.callback(x), "", "Prestamos"],             
            ["home", lambda x: app.ChangePage("InitialPage", "Inicio"), "", "Inicio"],    
            ["cash-register", lambda x: app.callback(x), "", "Cajero"],             
            ["store", lambda x: app.callback(x), "", "Almacen"],             
            ]

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager

            MDScreen:
                name: "InitialPage"

                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, 1
                    MDGridLayout:
                        cols: 1
                        padding: dp(0), dp(toolbar.height), dp(0), dp(toolbarbottom.height)
                        MDBoxLayout:
                            adaptive_height: True               
                            size_hint: 1, 1

                            MDGridLayout:
                                cols: 1                                
                                
                                MDLabel:
                                    markup: True
                                    padding: dp(50), dp(20), dp(16), dp(1)
                                    text: "[b][i]Datos[/i][/b]"      
                                    halign: "left"
                                    font_style: "H3"
                                    adaptive_height: True       

                                MDBoxLayout:
                                    orientation: 'horizontal'
                                    size_hint: 1, None
                                    height:75


                                    MDGridLayout:
                                    
                                        cols: 2                             
                                        padding: dp(1), dp(10), dp(1), dp(1)


                                        MDBoxLayout:
                                            padding: dp(50), dp(1), dp(25), dp(1)

                                            MDIcon:
                                                padding: dp(1), dp(1), dp(10), dp(1)
                                                icon: "account"
                                                pos_hint: {"center_x": .5, "center_y": .75} 
                                                font_size: '36sp' 
                                            MDTextField:
                                                pos_hint: {"center_x": 1, "center_y": .7} 
                                                text: "root"
                                                hint_text: "Nombre de usuario:"
                                                mode: "rectangle"
                                                disabled: True 
                                                focus: True

                                        MDBoxLayout:

                                            padding: dp(25), dp(1), dp(50), dp(1)

                                            MDIcon:
                                                padding: dp(1), dp(1), dp(10), dp(1)
                                                icon: "account-hard-hat"
                                                pos_hint: {"center_x": .5, "center_y": .75} 
                                                font_size: '36sp' 
                                            MDTextField:
                                                pos_hint: {"center_x": 1, "center_y": .7} 
                                                text: "root"
                                                hint_text: "Nivel de usuario:"
                                                mode: "rectangle"
                                                disabled: True 
                                                focus: True
                                            

                                MDLabel:                                
                                    markup: True
                                    padding: dp(50), dp(1), dp(1), dp(1)
                                    text: "[b][i]Cuenta[/i][/b]"
                                    halign: "left"
                                    font_style: "H3"
                                    adaptive_height: True             

                                MDBoxLayout:
                                    orientation: 'horizontal'
                                    size_hint: 1, None
                                    height:75


                                    MDGridLayout:
                                    
                                        cols: 2                             
                                        padding: dp(1), dp(10), dp(1), dp(1)


                                        MDBoxLayout:
                                            padding: dp(50), dp(1), dp(25), dp(1)

                                            MDIcon:
                                                padding: dp(1), dp(1), dp(10), dp(1)
                                                icon: "cash-plus"
                                                pos_hint: {"center_x": .5, "center_y": .75} 
                                                font_size: '36sp' 
                                            MDTextField:
                                                pos_hint: {"center_x": 1, "center_y": .7} 
                                                text: "100$"
                                                hint_text: "Dinero Credito:"
                                                mode: "rectangle"
                                                disabled: True 
                                                focus: True

                                        MDBoxLayout:

                                            padding: dp(25), dp(1), dp(50), dp(1)

                                            MDIcon:
                                                padding: dp(1), dp(1), dp(10), dp(1)
                                                icon: "cash-minus"
                                                pos_hint: {"center_x": .5, "center_y": .75} 
                                                font_size: '36sp' 
                                            MDTextField:
                                                pos_hint: {"center_x": 1, "center_y": .7} 
                                                text: "24$"
                                                hint_text: "Dinero prestado:"
                                                mode: "rectangle"
                                                disabled: True 
                                                focus: True
                                
                                MDBoxLayout:
                                    orientation: 'horizontal'
                                    size_hint: 1, None
                                    height:75

                                    MDGridLayout:
                                    
                                        cols: 3                            
                                        padding: dp(1), dp(10), dp(1), dp(1)

                                        MDBoxLayout:
                                            padding: dp(50), dp(1), dp(1), dp(1)

                                            MDIcon:
                                                padding: dp(1), dp(1), dp(10), dp(1)
                                                icon: "cash"
                                                pos_hint: {"center_x": .5, "center_y": .75} 
                                                font_size: '36sp' 
                                            MDTextField:
                                                pos_hint: {"center_x": .5, "center_y": .7} 
                                                text: "100$"
                                                hint_text: "Dinero en dólares:"
                                                mode: "rectangle"
                                                disabled: True 
                                                focus: True
                                    
                                        MDBoxLayout:
                                            padding: dp(30), dp(1), dp(30), dp(1)

                                            MDIcon:
                                                padding: dp(1), dp(1), dp(10), dp(1)
                                                icon: "cash"
                                                pos_hint: {"center_x": .5, "center_y": .75} 
                                                font_size: '36sp' 
                                            MDTextField:
                                                pos_hint: {"center_x": .5, "center_y": .7} 
                                                text: "100$"
                                                hint_text: "Dinero en pesos:"
                                                mode: "rectangle"
                                                disabled: True 
                                                focus: True
                                        
                                        MDBoxLayout:
                                            padding: dp(1), dp(1), dp(50), dp(1)

                                            MDIcon:
                                                padding: dp(1), dp(1), dp(10), dp(1)
                                                icon: "cash"
                                                pos_hint: {"center_x": .5, "center_y": .75} 
                                                font_size: '36sp' 
                                            MDTextField:
                                                pos_hint: {"center_x": .5, "center_y": .7} 
                                                text: "100$"
                                                hint_text: "Dinero en bolívares:"
                                                mode: "rectangle"
                                                disabled: True 
                                                focus: True

                                MDBoxLayout:
                                    orientation: 'horizontal'
                                    size_hint: 1, None
                                    height:75

                                    MDGridLayout:
                                    
                                        cols: 1                            
                                        padding: dp(1), dp(10), dp(1), dp(1)

                                        MDBoxLayout:
                                            padding: dp(230), dp(1), dp(230), dp(1)

                                            MDIcon:
                                                padding: dp(1), dp(1), dp(10), dp(1)
                                                icon: "cash"
                                                pos_hint: {"center_x": .5, "center_y": .8} 
                                                font_size: '36sp' 
                                            MDTextField:
                                                pos_hint: {"center_x": .5, "center_y": .7} 
                                                text: "100$"
                                                hint_text: "Dinero mensual:"
                                                mode: "rectangle"
                                                disabled: True 
                                                focus: True

            MDScreen:
                name: "StorePageUpdate"
                
                MDLabel:
                    text: "Screen 2"
                    halign: "center"

            MDScreen:
                name: "StorePage"

                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, 1
                    MDGridLayout:
                        cols: 1
                        padding: dp(16), dp(toolbar.height), dp(16), dp(toolbarbottom.height)
                                
                        MDGridLayout:
                            cols: 3
                            spacing: dp(20)
                            padding: dp(16), dp(16), dp(16), dp(16)
                            size_hint_y: None
                            height: dp(toolbar.height)
                            MDTextField:
                                id: ButtonMenuSearchingStore

                                size_hint_x: None
                                width: "100dp"

                                text: "TODO"
                                hint_text: "Tipo:"
                                icon_right: "arrow-down"

                                mode: "rectangle"
                                readonly: True 
                                focus: True


                                on_focus: if self.focus: app.MenuProductoTypeStore.open()

                            MDTextField:
                                id: SearchProduct
                                hint_text: 'Buscar producto'
                                icon_right: "android"
                                mode: "rectangle"

                            MDFloatingActionButton:
                                id: ButtonSearchingStore

                                width: "150dp"
                                icon: "book-search"
                                style: "standard"
                                width: "100dp"
                                
                        ClientsTable:

                                            

                               

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
        
            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer

                
'''

#VARIABLE QUE ALMACENA EL SELF, PERMITE CAMBIAR DE SCREN (PANTALLA) AUN SI SON DIFERENTES CLASES
global_self = ''

class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

#PERMITE MOSTRAR EL ICONO EN LOS SELECTS DE TASA DE DINERO
class Item(OneLineAvatarIconListItem):
    left_icon = StringProperty()


class App(MDApp):

    #LO PRIMERO QUE SE CARGA
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #CARGA LOS DATOS DE .KV
        self.screen = Builder.load_string(KV)

        #PROCESO QUE ALMACENA DE FORMA GLOBAL LOS DATOS DE SELF EN GLOBAL_SELF
        global global_self
        global_self = self

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
                "on_press": lambda x='TODO': self.ChangeSearchingTypeStore(x),
            },
            {
                "text": "CANTIDAD ASC",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='CANTIDAD ASC': self.ChangeSearchingTypeStore(x),
            },
            {
                "text": "CANTIDAD DES",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='CANTIDAD DES': self.ChangeSearchingTypeStore(x),
            },
            {
                "text": "PRECIO ASC",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='PRECIO ASC': self.ChangeSearchingTypeStore(x),
            },
            {
                "text": "PRECIO DES",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='PRECIO DES': self.ChangeSearchingTypeStore(x),
            },
        ]
        self.MenuProductoTypeStore = MDDropdownMenu(
            caller=self.screen.ids.ButtonMenuSearchingStore,
            border_margin=dp(4),
            items=menu_items3,
            hor_growth="right",
            ver_growth="down",
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
    def ChangePage(self, page, text, dontSelf = None):


        if dontSelf == None:
            self.root.ids.screen_manager.current = page
            self.root.ids.toolbar.title = text

            global global_self
            global_self = self

        elif dontSelf == True:

            match page:
                case 'StorePageUpdate':
                    ClientsTable.CloseDialogStorePage('obj')
                case _:
                    pass

            global_self.root.ids.screen_manager.current = page
            global_self.root.ids.toolbar.title = text

    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeStore(self, instace):
        
        self.root.ids.ButtonMenuSearchingStore.text = instace
        self.MenuProductoTypeStore.dismiss()

    def test(self):
            print('funcionó')
    

## CLASE PARA MOSTRAR LA TABLA, MDDATATABLE
class ClientsTable(Screen):

    dialog = None
    dialog2 = None
    dialog3 = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #print('entro en load_table')
        layout = MDAnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 1, 'center_x': 1},
            size_hint=(1, 1),
            padding= [dp(16), dp(32)],
            use_pagination=True,
            column_data=[
                ("Imagen", dp(30)),
                ("Nombre", dp(30)),
                ("Proveedor", dp(30)),
                ("Cantidad", dp(30)),
                ("Precio", dp(15)),
            ],
            row_data=[
                (
                    "imagen.jpg",
                    "Arroz",
                    "Polar S.A.",
                    "42",
                    "62.5",
                )
                for i in range(50)],)
        
        self.data_tables.bind(on_row_press=self.on_row_press)
        layout.add_widget(self.data_tables)
        self.add_widget(layout)
        #return layout

    def on_row_press(self, instance_table, instance_row):
        self.ShowAlertDialog()

        print(instance_table, instance_row)


    def ShowAlertDialog(self):
        
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
                        on_release= lambda x: App.ChangePage(x,"StorePageUpdate", "Almacen", True)
                                                        
                    ),
                ],
            )
        self.dialog.open()

    def ShowAlertDialogDelete(self, obj):

        self.CloseDialogStorePage('obj')

        if not self.dialog2:
            self.dialog2 = MDDialog(
                title="¿De verdad quiere eliminar este producto?",
                text="Si es así, adelante",
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        text_color=self.theme_cls.primary_color,
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

App().run()