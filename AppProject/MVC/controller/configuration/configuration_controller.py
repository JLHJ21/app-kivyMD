from kivy.properties import StringProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

import MVC.controller.functions as functions
from MVC.model.configuration.configuration_model import ConfigurationBD 


#PAGINA DE CONFIGURACION
class ConfigurationPage(MDScreen):

    dialogUsername = dialogPassword = dialogEmail = None

    username_text =  email_text = password_text = ''

    def on_pre_enter(self):

        if functions.have_session == True:

            self.UpdateDataUser()
            #self.ids.passwordConfiguration.text = functions.password_text

            print('puede entrar')
        else:
            print('no puede entrar')
            functions.FunctionsKivys.ChangePage('SignInPage', 'Iniciar Sesión')

    def OpenModal(self, inputOneName, inputTwoName, dialogName, title):

        ContentConfigurationPage.Variables(inputOneName, inputTwoName)

        match dialogName:
            case 'dialogUsername':
                self_name = self.dialogUsername
                indexData = 'username'
            
            case 'dialogEmail':
                self_name = self.dialogEmail
                indexData = 'email'
            
            case 'dialogPassword':
                self_name = self.dialogPassword
                indexData = 'password'

            case _:
                self_name = self.dialogUsername
                indexData = 'username'


        if not self_name:
            self_name = MDDialog(
                title=title,
                type="custom",
                content_cls=ContentConfigurationPage(),
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        md_bg_color="red",
                        text_color="white",
        
                        on_release = lambda x='': self.CloseDialog(self_name)
                    ),
                    MDRaisedButton(
                        text="Aceptar",
                        md_bg_color="blue",
                        on_release= lambda x='': self.OptionsChageUserData(indexData, global_self_content_configuration.ids.inputOne.text, global_self_content_configuration.ids.inputTwo.text, self_name)
                        #text_color=self.theme_cls.primary_color,
                    ), 
                ],
            )
        self_name.open()

    def OptionsChageUserData(self, indexData, value1, value2, self_dialog):

        ConfigurationBD.ChangeUserData(indexData, value1, value2)
        self.UpdateDataUser()
        self.CloseDialog(self_dialog)

    def CloseDialog(self, self_dialog):
        self_dialog.dismiss()


    def UpdateDataUser(self):
        print('UpdateDataUser')
        self.ids.usernameConfiguration.text = functions.username_text
        self.ids.emailConfiguration.text = functions.email_text
        

global_self_content_configuration = None
class ContentConfigurationPage(MDBoxLayout):



    inputOne= StringProperty(None)
    inputTwo= StringProperty(None)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        global global_self_content_configuration
        global_self_content_configuration = self

    
    def Variables(nameInputOne, nameInputTwo):
        ContentConfigurationPage.inputOne = nameInputOne
        ContentConfigurationPage.inputTwo = nameInputTwo


        #print(ContentConfigurationPage.inputOne )