class MenuAndTitleSelect():

    def DropMenu(self, button, DropMenu):

        DropMenu.caller = button
        DropMenu.open()


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeNameDropMenu(self, DropMenu, IdButton, Text = ""):
        
        self.ids[IdButton].text = Text
        DropMenu.dismiss()

#Archivo intermediario para obtener el self en cada uno de los archivos python
global_variable_self = None
have_session = False

class GlobalVariables():

    def GetGlobalSelf(self):
        
        global global_variable_self
        global_variable_self = self

    def GetVariable():
        return global_variable_self

class FunctionsKivys():
    
    def ChangePage(current_screen, title_screen):

        self_main = GlobalVariables.GetVariable()
        
        #obtiene el self principal del kivy
        #self_main = self.global_variable_self

        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = current_screen

        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = title_screen


#Variables 'globales' de los datos del usuario
username_text = email_text = password_text = ''
access_text = 0
