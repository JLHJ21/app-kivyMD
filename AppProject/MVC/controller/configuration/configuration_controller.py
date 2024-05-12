from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import StringProperty

#PAGINA DE CONFIGURACION
class ConfigurationPage(MDScreen):

    dialogUsername = dialogPassword = dialogEmail = None

    def OpenModal(self, inputOneName, inputTwoName, dialogName, title):
        ContentConfigurationPage.Variables(inputOneName, inputTwoName)

        match dialogName:
            case 'dialogUsername':
                self_name = self.dialogUsername
            
            case 'dialogEmail':
                self_name = self.dialogEmail
            
            case 'dialogPassword':
                self_name = self.dialogPassword

            case _:
                self_name = self.dialogUsername


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
                    ),
                    MDRaisedButton(
                        text="Aceptar",
                        md_bg_color="blue",
                        #text_color=self.theme_cls.primary_color,
                    ),
                ],
            )
        self_name.open()

class ContentConfigurationPage(MDBoxLayout):



    inputOne= StringProperty(None)
    inputTwo= StringProperty(None)

    
    def Variables(nameInputOne, nameInputTwo):
        ContentConfigurationPage.inputOne = nameInputOne
        ContentConfigurationPage.inputTwo = nameInputTwo


        #print(ContentConfigurationPage.inputOne )