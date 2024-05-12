from kivymd.uix.screen import MDScreen

#PAGINA DE HISTORIAL DE DINERO/DIVISAS
class MoneyHistoryPage(MDScreen):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_money_history
        self_money_history = self

    
    def ChangeTypeHistoryMoney(self):

        textTitle = self_money_history.ids.MoneyHistoryTitle.text

        match textTitle:
            case 'MES':
                variableTitle = 'TOTAL'
                variableLabelSales = '100'
                variableLabelCharge = '-60'
                variableTotalMoney = '40'
                variableChangeTypeMoneyHistory = 'Cambiar a: MES'

            case 'TOTAL':

                variableTitle = 'MES'
                variableLabelSales = '1000'
                variableLabelCharge = '-600'
                variableTotalMoney = '400'
                variableChangeTypeMoneyHistory = 'Cambiar a: TOTAL'
            case _:
                pass



        self_money_history.ids.MoneyHistoryTitle.text = variableTitle

        self_money_history.ids.LabelSalesProducts.text = variableLabelSales

        self_money_history.ids.LabelChargeProducts.text = variableLabelCharge

        self_money_history.ids.LabelTotalMoney.text = variableTotalMoney

        self_money_history.ids.buttonChangeTypeMoneyHistory.text = variableChangeTypeMoneyHistory



