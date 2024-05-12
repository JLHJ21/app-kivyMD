from kivy.clock import Clock
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

import MVC.controller.functions as functions

#PAGINA DE PRESTAMOS
class LoanPage(MDScreen):


    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        Clock.schedule_once(lambda dt: self.ChangeItemsGrid('mes'))

    def ChangePageLoanPage(self):

        #obtiene el self principal del kivy
        self_main = functions.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = 'LoanAddPage'
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = 'Prestamo - Agregar'

    def ChangeItemsGrid(self, typeLoan):


        self.ids.gridLayoutLoanItems.clear_widgets()


        match typeLoan:
            case 'total':
                self.ids.buttonChangeTypeMoneyHistory.text = "Cambiar a: MES"
                self.ids.MoneyHistoryTitle.text = 'TOTAL'
                textAmountMoney = 'total XXX'
                pass
            case 'mes':
                self.ids.buttonChangeTypeMoneyHistory.text = "Cambiar a: TOTAL"
                self.ids.MoneyHistoryTitle.text = 'MES'

                textAmountMoney = 'mes XXX'
                pass
            case _:
                self.ids.buttonChangeTypeMoneyHistory.text = "Cambiar a: TOTAL"
                self.ids.MoneyHistoryTitle.text = 'TOTAL'

                textAmountMoney = 'total XXX'
            
                pass

        for i in range(0, 5):
        
            NewGridLayout = MDGridLayout(
                cols= 2,
                spacing= dp(20),
                padding= [dp(16), dp(18)],

                size_hint_y= None,
                height= dp(40)
            )

            NewLabels1 = MDLabel(
                        size_hint_x= 0.4,
                        text= "Ventas",
                        halign= "left",
                        font_style= "H6",
                    )
            

            NewLabels2 = MDLabel(

                    size_hint_x= 0.4,
                    halign= "right",

                    text= textAmountMoney,
                    mode= "rectangle",
                )



            NewGridLayout.add_widget(NewLabels1)
            NewGridLayout.add_widget(NewLabels2)

            self.ids.gridLayoutLoanItems.add_widget(NewGridLayout)


        NewLabels3 = MDLabel(
                        size_hint_x= 0.4,
                    )
            

        NewLabels4 = MDLabel(
                padding= [ dp(1), dp(40), dp(1), dp(1)],

                size_hint_x= 0.4,
                halign= "right",

                text= textAmountMoney,
                mode= "rectangle",
                underline= True,

            )
        

        NewGridLayout.add_widget(NewLabels3)
        NewGridLayout.add_widget(NewLabels4)

