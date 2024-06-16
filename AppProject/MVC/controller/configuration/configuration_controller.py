from kivy.properties import StringProperty, NumericProperty, BooleanProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

import MVC.controller.functions as functions
from MVC.model.configuration.configuration_model import ConfigurationBD 
from kivymd.toast.kivytoast.kivytoast import toast

from kivy.app import App
import re
from passlib.hash import sha256_crypt

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

#PAGINA DE CONFIGURACION
class ConfigurationPage(MDScreen):

    dialog = None

    #dialogUsername = dialogPassword = dialogEmail = None

    #username_text =  email_text = password_text = ''

    def on_pre_enter(self):

        if functions.have_session == True:
            self.UpdateDataUser()
            #self.ids.passwordConfiguration.text = functions.password_text

        else:
            toast('No tiene una sesión activa.')
            functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')

    def OpenModal(self, inputOneName, inputTwoName, dialogName, title):

        self_page = App.get_running_app().root.ids.screen_manager.get_screen('ConfigurationPage')

        match dialogName:
            case 'dialogUsername':
                #self_name = self.dialogUsername
                indexData = 'username'
            
            case 'dialogEmail':
                #self_name = self.dialogEmail
                indexData = 'email'
            
            case 'dialogPassword':
                #self_name = self.dialogPassword
                indexData = 'password'

            case _:
                #self_name = self.dialogUsername
                indexData = 'username'

        ContentConfigurationPage.Variables(inputOneName, inputTwoName, indexData)

        #if not self_name:
        self_page.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=ContentConfigurationPage(),
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    md_bg_color="red",
                    text_color="white",
    
                    on_release = lambda x='': self.CloseDialog(self_page.dialog)
                ),
                MDRaisedButton(
                    text="Aceptar",
                    md_bg_color="blue",
                    on_release= lambda x='': self.OptionsChageUserData(indexData, global_self_content_configuration.ids.inputOne.text, global_self_content_configuration.ids.inputTwo.text, self_page.dialog)
                    #text_color=self.theme_cls.primary_color,
                ), 
            ],
        )
        self_page.dialog.open()

    def OptionsChageUserData(self, indexData, value1, value2, self_dialog):

        #validacion usuario
        if indexData == 'username':

            if len(value1) < 5:
                toast('Hubo un error, el usuario tiene que ser minimo de 5 caracteres.')
                return
            
            elif len(value1) > 20:
                toast('Hubo un error, el campo usuario se excede de caracteres.')
                return
            elif value2 == '':
                toast('Hubo un error, el segundo campo no puede estar vacío')
                return
        
            elif value1 == functions.usernameStaff:
                toast('Hubo un error, el usuario es el mismo.')
                return

            
        #validacion correo electronico    
        elif indexData == 'email':
            if re.fullmatch(regex, value1) == None:
                toast('El correo electrónico no es válido.')
                return

            if len(value1) < 5:
                toast('El correo electrónico tiene que ser mínimo de 5 caracteres.')
                return
            
            elif len(value1) > 35:
                toast('El campo correo se excede de caracteres.')
                return
            elif value2 == '':
                toast('Hubo un error, el segundo campo no puede estar vacío')
                return
            elif value1 == functions.emailStaff:
                toast('Hubo un error, el correo electrónico es el mismo.')
                return

        elif indexData == 'password':
            if len(value1) < 5:
                toast('La contraseña tiene que ser minimo de 5 caracteres.')
                return
            
            elif len(value1) > 20:
                toast('El campo contraseña se excede de caracteres.')
                return
            
            elif value2 == '':
                toast('Hubo un error, el segundo campo no puede estar vacío')
                return
            
            elif sha256_crypt.verify(value1, functions.passwordStaff):
                toast('Hubo un error, la contraseña es la misma.')
                return
                    
        ###########

        if not value1 == value2:
        
            toast('Hubo un error, los datos no son iguales.')
            return
        else:


            #Si no hay errores en validacion, utiliza este codigo
            result = ConfigurationBD.ChangeUserData(indexData, value1, value2)

            if result == True:
                toast('¡Se ha cambiado el dato con éxito!')
                self.UpdateDataUser()
                self.CloseDialog(self_dialog)
            else:
                toast('Hubo un error' + str(result))
            


    def CloseDialog(self, self_dialog):
        self_dialog.dismiss()


    def UpdateDataUser(self):
        self.ids.usernameConfiguration.text = functions.usernameStaff
        self.ids.emailConfiguration.text = functions.emailStaff
        

global_self_content_configuration = None
class ContentConfigurationPage(MDBoxLayout):



    inputOne= StringProperty(None)
    inputTwo= StringProperty(None)

    textMaximumOne = NumericProperty(0)
    textMaximumTwo = NumericProperty(0)

    passwordOne = BooleanProperty(False)
    passwordTwo = BooleanProperty(False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        global global_self_content_configuration
        global_self_content_configuration = self

    
    def Variables(nameInputOne, nameInputTwo, typeInput):
        ContentConfigurationPage.inputOne = nameInputOne
        ContentConfigurationPage.inputTwo = nameInputTwo

        


        match typeInput:
            case 'password':

                ContentConfigurationPage.textMaximumOne = 20
                ContentConfigurationPage.textMaximumTwo = 20


                ContentConfigurationPage.passwordOne = True
                ContentConfigurationPage.passwordTwo = True
                
            case 'email':

                ContentConfigurationPage.textMaximumOne = 35
                ContentConfigurationPage.textMaximumTwo = 35


                ContentConfigurationPage.passwordOne = False
                ContentConfigurationPage.passwordTwo = False
                
            case 'username':
                
                ContentConfigurationPage.textMaximumOne = 20
                ContentConfigurationPage.textMaximumTwo = 20


                ContentConfigurationPage.passwordOne = False
                ContentConfigurationPage.passwordTwo = False
                
        #print(ContentConfigurationPage.inputOne )