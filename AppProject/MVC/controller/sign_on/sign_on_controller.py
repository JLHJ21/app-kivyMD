
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView

from MVC.model.sign_on.sign_on_model import SignOnDatabase
from passlib.hash import sha256_crypt

import MVC.controller.functions as functions

from kivymd.toast.kivytoast.kivytoast import toast

import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

class ScrollViewCustom(MDScrollView):
    pass

#PAGINA DE REGISTRAR CUENTA
class SignOnPage(MDScreen):

    def ChangePageToSignIn(self):
        functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')

    
    def CreateAccount(self, username, email, password, password2):

        #VALIDACIONES
        #usuario
        if username == '' or len(username) < 5:
            toast('El usuario tiene que ser minimo de 5 caracteres.')
        elif len(username) > 20:
            toast('El campo usuario se excede de caracteres.')

        #email
        elif re.fullmatch(regex, email) == None:

            toast_variable = 'El correo electrónico no es válido.'

            if len(email) < 5:
                toast_variable = 'El correo electrónico tiene que ser mínimo de 5 caracteres.'
            elif len(email) > 35:
                toast_variable = 'El campo correo se excede de caracteres.'
            toast(toast_variable)

        #contraseña
        elif password == '' or len(password) < 5:
            toast('La contraseña tiene que ser minimo de 5 caracteres.')
        elif len(password) > 20:
            toast('El campo contraseña se excede de caracteres.')

        else:
            if password == password2:
                password = sha256_crypt.hash(password)
                result = SignOnDatabase.CreateAccountDB(username, email, password)

                if result == True:
                    self.ChangePageToSignIn()
                else:
                    toast('Hubo un error' + str(result) + '.')
            else:
                toast('Las contraseñas no son idénticas.')