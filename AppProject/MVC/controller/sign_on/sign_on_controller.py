
from kivymd.uix.screen import MDScreen
from MVC.model.sign_on.sign_on_model import SignOnDatabase
from passlib.hash import sha256_crypt


import MVC.controller.functions as functions

#PAGINA DE REGISTRAR CUENTA
class SignOnPage(MDScreen):

    def ChangePageToSignIn(self):
        functions.FunctionsKivys.ChangePage('SignInPage', 'Iniciar Sesión')

    
    def CreateAccount(self, username, email, password, password2):


        if password == password2:
            
            password = sha256_crypt.hash(password)
            result = SignOnDatabase.CreateAccountDB(username, email, password)

            if result == True:
                self.ChangePageToSignIn()

            print(result)
        else:
            pass