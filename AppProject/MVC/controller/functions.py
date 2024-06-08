class MenuAndTitleSelect():

    def DropMenu(self, button, DropMenu):

        DropMenu.caller = button
        DropMenu.open()


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeNameDropMenu(self, DropMenu, IdButton, Text = ""):
        
        self.ids[IdButton].text = Text
        DropMenu.dismiss()

#Archivo intermediario para obtener el self en cada uno de los archivos python
global_variable_self = global_bolivar = global_peso = global_dolar = None
have_session = False

class GlobalVariables():

    def GetGlobalSelf(self):
        
        global global_variable_self
        global_variable_self = self

    def GetVariable():
        return global_variable_self

    def AddForeignExchange(bolivar, peso, dolar):
        global  global_bolivar, global_peso, global_dolar

        global_bolivar = bolivar
        global_peso = peso
        global_dolar = dolar

class FunctionsKivys():
    
    def ChangePage(self, current_screen, title_screen):

        import MVC.controller.header_footer.header_footer_controller as HeaderAndFooter

        self_main = GlobalVariables.GetVariable()
        
        #obtiene el self principal del kivy
        #self_main = self.global_variable_self

        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = current_screen
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = title_screen
        
        HeaderAndFooter.HeaderAndFooter.titleHeader = title_screen


#Variables 'globales' de los datos del usuario
usernameStaff = emailStaff = passwordStaff = idStaff = ''
access_text = 0
