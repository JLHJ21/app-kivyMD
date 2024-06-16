from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

import MVC.controller.functions as functions
from kivymd.toast.kivytoast.kivytoast import toast



class ScrollViewCustom(MDScrollView):
    pass

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

            self.ids.usernameHomeLabel.text = functions.usernameStaff
            self.ids.accessLevelHomeLabel.text = access_text_string
            
        else:
            toast('No tiene una sesión activa.')
            functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')

    