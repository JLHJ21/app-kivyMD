#Archivo intermediario para obtener el self en cada uno de los archivos python
global_variable_self = None

class GlobalVariables():

    def GetGlobalSelf(self):
        
        global global_variable_self
        global_variable_self = self