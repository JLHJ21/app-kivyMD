
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

class GlobalVariables():

    def GetGlobalSelf(self):
        
        global global_variable_self
        global_variable_self = self