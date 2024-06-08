from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.clock import Clock

import MVC.controller.functions as functions

#MENU LATERAL
class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


#CABECERA Y PIE DE PAGINA DE LA PAGINA
class HeaderAndFooter(MDScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(lambda dt: self.MenusSelects())
    
    def MenusSelects(self):

        self_main = functions.global_variable_self

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
        self_main.menu_foreign_exchange = MDDropdownMenu(
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
                "on_press": lambda x='Item configuracion': functions.FunctionsKivys.ChangePage('self', 'ConfigurationPage', 'Configuración'),
            },
            {
                "text": "Cerrar Sesión",
                "leading_icon": "account-arrow-left",
                "on_press": lambda x='Item perfil': self.CloseSession(),
            },
        ]
        self_main.menu_configuration_header = MDDropdownMenu(
            border_margin=dp(4),
            items=menu_configuration_header,
            width=dp(240),
            hor_growth="left",
            #radius=[24, 0, 24, 24],
            elevation= 4
        )
        
    def CallbackTypeMoney(self, action = None):

        self_main = functions.global_variable_self

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
        
        self_main.root.ids.toolbar.right_action_items[0] = items[0]
        self_main.menu_foreign_exchange.dismiss()

    #Callbacks de los botones
    #####################
    def CallbackMenuChangeMoney(self, button):

        self_main = functions.global_variable_self
        
        self_main.menu_foreign_exchange.caller = button
        self_main.menu_foreign_exchange.open()

    def CallbackMenuUser(self, button):

        self_main = functions.global_variable_self
        
        self_main.menu_configuration_header.caller = button
        self_main.menu_configuration_header.open()
    #####################


    def CloseSession(self):

        self_main = functions.global_variable_self

        functions.have_session = False
        functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')

        self_main.menu_configuration_header.dismiss()
