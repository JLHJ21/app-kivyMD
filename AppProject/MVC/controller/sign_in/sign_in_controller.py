
from kivymd.uix.screen import MDScreen
from MVC.model.sign_in.sign_in_model import SignInDatabase


import MVC.controller.functions as functions

#PAGINA DE INICIAR SESION
class SignInPage(MDScreen):


    def ChangePageToSignOn(self):
        functions.FunctionsKivys.ChangePage('SignOnPage', 'Registrarse')


    def SignIn(self, username, password):
        result = SignInDatabase.SignInBD(username, password)
        
        if result == True:
            self.OpenSystem()
        else:
            print('no coinciden')


    def OpenSystem(self):

        functions.have_session = True

        functions.FunctionsKivys.ChangePage('InitialPage', 'Panel de Control')

        #obtiene el self principal del kivy
        #self_main = functions.global_variable_self
        #self_main.root.ids.screen_manager.current = 'InitialPage'

    pass