import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor()

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

rate_bolivar = rate_dolar = money_preference = last_change = None

have_session = False

class GlobalVariables():

    def GetGlobalSelf(self):
        
        global global_variable_self
        global_variable_self = self

    def GetVariable():
        return global_variable_self
    
    def UpdateForeignExchange(bolivar, dolar, preference, new_change):

        global rate_bolivar, rate_dolar, money_preference, last_change
        '''
        Para obtener el valor en BOLIVARES, se divide el precio en PESOS por la tasa en BOLIVARES

        Para obtener el valor en DOLARES, se divide el precio en PESOS por la tasa en PESOS

        Para obtener el valores PESOS, se multiplica el valor por uno (1), ya que ya los precios son dados así

        El valor PREFERENCE permite saber como se tiene que tratar el valor al retirarlo de la base de datos
        '''

        bolivar = FunctionsKivys.TransformProfit(bolivar, 'float')
        rate_bolivar = bolivar

        #rate_bolivar = peso
        dolar = FunctionsKivys.TransformProfit(dolar, 'float')
        rate_dolar = dolar

        money_preference = preference
        last_change = new_change

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

    def TransformProfit(string_variable, type_transform):

        #Me transform el texto para usar el float
        # Ejemplo: 4.500,00 -> 4500.00
        if type_transform == 'float':
        
            #cambia punto por nada
            string_variable = string_variable.replace('.', '')
            #cambia la coma por .
            string_variable = string_variable.replace(',', '.')

        #Me transform el texto para ser visualizado por el usuario
        # Ejemplos: 4500.00 -> 4.500,00
        elif type_transform == 'human':

            string_variable = float(string_variable)
            string_variable = "{:0,.2f}".format(string_variable)

            #cambia la coma por _
            string_variable = string_variable.replace(',', '_')
            #cambia punto por coma
            string_variable = string_variable.replace('.', ',')
            #cambia _ por punto
            string_variable = string_variable.replace('_', '.')

        return string_variable

    def ChangeCommaAndDot(string_variable, inversed):
        if inversed == False:

            
            #cambia punto por nada
            string_variable = string_variable.replace('.', '')
            #cambia la coma por .
            string_variable = string_variable.replace(',', '.')

            string_variable = float(string_variable)
            string_variable = "{:0,.2f}".format(string_variable)


            #cambia la coma por _
            string_variable = string_variable.replace(',', '_')
            #cambia punto por coma
            string_variable = string_variable.replace('.', ',')
            #cambia _ por punto
            string_variable = string_variable.replace('_', '.')

            '''
            #cambia la coma por _
            string_variable = string_variable.replace(',', '_')
            #cambia punto por coma
            string_variable = string_variable.replace('.', ',')
            #cambia _ por punto
            string_variable = string_variable.replace('_', '.')
            '''
        else:
            #cambia la coma por _
            string_variable = string_variable.replace('.', '_')
            #cambia punto por coma
            string_variable = string_variable.replace(',', '.')
            #cambia _ por punto
            string_variable = string_variable.replace('_', ',')

        return string_variable

    def TransformMoney(moneyToTransform, typeMoney = True):
        #usar la variable de money_preference con un match y se multiplica/divide con el valor obtenido de la base de datos (valor siempre en pesos)
        #profit = moneyToTransform['profit_product']

        if typeMoney == True:
            match money_preference:
                case 'bolivar':
                    new_profit = float(moneyToTransform) / float(rate_bolivar)
                    new_profit = f"{new_profit:.2f}"

                case 'dolar':
                    new_profit = float(moneyToTransform) / float(rate_dolar)
                    new_profit = f"{new_profit:.2f}"
                case 'peso':
                    new_profit = moneyToTransform
                    #new_profit = f"{new_profit:.3f}"
        else:
            
            match typeMoney:
                case 'Bolívar':
                    new_profit = float(moneyToTransform) / float(rate_bolivar)
                    new_profit = f"{new_profit:.2f}"

                case 'Dólar':
                    new_profit = float(moneyToTransform) / float(rate_dolar)
                    new_profit = f"{new_profit:.2f}"
                case 'Peso':
                    new_profit = moneyToTransform
                    #new_profit = f"{new_profit:.3f}"

                #CAMBIAR
                case 'bolivar':
                    new_profit = float(moneyToTransform) / float(rate_bolivar)
                    new_profit = f"{new_profit:.2f}"

                case 'dolar':
                    new_profit = float(moneyToTransform) / float(rate_dolar)
                    new_profit = f"{new_profit:.2f}"
                case 'peso':
                    new_profit = moneyToTransform
                    #new_profit = f"{new_profit:.3f}"

            #Valor en pesos
            #new_profit = float(moneyToTransform) / float(rate_dolar)
            #new_profit = f"{new_profit:.3f}"


        #results['profit_product'] = str(new_profit)
        return str(new_profit)


#Variables 'globales' de los datos del usuario
usernameStaff = emailStaff = passwordStaff = idStaff = ''
access_text = 0
