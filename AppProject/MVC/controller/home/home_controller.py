from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

import MVC.controller.functions as functions


#PAGINA DE INICIO
class InitialPage(MDScreen):    

    def on_pre_enter(self):

        if functions.have_session == True:

            access_text_string = ''

            
            match functions.access_text:
                case 0:
                    access_text_string = 'Empleado'
                case 1:
                    access_text_string = 'Administrador'
                case 2:
                    access_text_string = 'Programador'
                case _:
                    access_text_string = 'Empleado'

            self.ids.usernameHomeLabel.text = functions.username_text
            self.ids.accessLevelHomeLabel.text = access_text_string
            print('puede entrar')
        else:
            print('no puede entrar')
            functions.FunctionsKivys.ChangePage('SignInPage', 'Iniciar Sesión')

    