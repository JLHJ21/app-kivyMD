
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from MVC.model.sign_in.sign_in_model import SignInDatabase


import MVC.controller.functions as functions
from kivymd.toast.kivytoast.kivytoast import toast


class ScrollViewCustom(MDScrollView):
    pass


#PAGINA DE INICIAR SESION
class SignInPage(MDScreen):

    def on_pre_enter(self):
        if functions.have_session == True:
            toast('Ya tiene una sesión activa.')
            functions.FunctionsKivys.ChangePage('self', 'InitialPage', 'Inicio')


    def ChangePageToSignOn(self):
        functions.FunctionsKivys.ChangePage('self', 'SignOnPage', 'Registrarse')


    def SignIn(self, username, password):
        
        #Validacion de inputs
        #usuario
        if username == '':
            toast('El campo usuario está vacío.')
        elif len(username) > 20:
            toast('El campo usuario se excede de caracteres.')

        #contraseña
        elif password == '':
            toast('El campo contraseña está vacío.')
        elif len(password) > 20:
            toast('El campo contraseña se excede de caracteres.')

        else:
            #llamada a la base de datos
            result = SignInDatabase.SignInBD(username, password)

            #si existe lo redirecciona a la pagina inicio
            if result == True:

                toast('¡Ha ingresado con éxito!')
                functions.have_session = True
                functions.FunctionsKivys.ChangePage('self', 'InitialPage', 'Inicio')

                #self.OpenSystem()
            else:
                toast('Los datos ingresados no coinciden.')



    #def OpenSystem(self):

    #    functions.have_session = True
    #    functions.FunctionsKivys.ChangePage('self', 'InitialPage', 'Panel de Control')

        #obtiene el self principal del kivy
        #self_main = functions.global_variable_self
        #self_main.root.ids.screen_manager.current = 'InitialPage'
