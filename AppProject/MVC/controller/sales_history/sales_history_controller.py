from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
import MVC.controller.functions as functions
import concurrent.futures
from MVC.model.sales_history.sales_history_model import SalesHistoryDB

from templates.table.table import RecycleViewTable
from kivy.metrics import dp
import weakref
from kivy.app import App
from kivymd.toast import toast

#PAGINA DE HISTORIAL DE VENTAS
class SalesHistoryPage(MDScreen):

    
    def on_pre_enter(self):
        if functions.have_session != True:
            toast('No tiene una sesión activa.')
            functions.FunctionsKivys.ChangePage('self', 'SignInPage', 'Iniciar Sesión')

    '''
        print()
        print()
        app= App.get_running_app()
        toolbar_height = (app.root.ids.toolbar.height)

        #table = MDLabel (
        #    text =' hola'
        #)
        
        table = RecycleViewTable(

            size_hint_y= None,
            height= dp(400),

            id_table= "tableSalesHistory",

            padding= [dp(16), dp(toolbar_height / 2), dp(16), dp(toolbar_height /2)],

            #objecto= self,
            need_image= False,
            columns= 4,
            #root= root,

            differentColumn= 'nothing',


            titles_labels= ["Cliente", "Empleado", "Monto", "Fecha"],
            list_table_data= ["name_client", "name_staff", "purchase", "date"],

            #Datos del Modal de eliminar "¿Esta seguro?"
            modalChooseDeleteConfirmationTitle= 'modalChooseDeleteConfirmationTitle',
            modalChooseDeletConfirmationeText= 'modalChooseDeletConfirmationeText',
            modalChooseDeleteConfirmation= 'print("modalChooseDeleteConfirmation")',

            modalChooseUpdate= 'print("modalChooseUpdate")',

            test= 'self.objecto.DictionaryDataset.update(self.objecto.root.ShowDataSalesHistoryController(self.objecto.StartPagination, self.objecto.StaticItemsAccountPagination, self.objecto.DirectionPagination))'
        )
        

        self.ids.gridLayoutContent.add_widget(table)
        self.ids.gridLayoutContent.ids.tableSalesHistory = weakref.ref(table)
        self.ids.gridLayoutContent.ids.tableSalesHistory.objecto = self.ids.gridLayoutContent.ids.tableSalesHistory


        print(self.ids.gridLayoutContent.ids.tableSalesHistory.objecto )
        #SalesHistoryDB.ShowDataSalesHistoryModel(0,5, '')
    '''
        
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global self_sales_history
        self_sales_history = self


    def CallbackMenuSalesHistory(self, button):

        functions.MenuAndTitleSelect.DropMenu("self", button, functions.global_variable_self.MenuTypeSalesHistory)


    ## CALLBACK DEL SELECT BUSCADOR DEL MENU ALMACEN
    def ChangeSearchingTypeSalesHistory(self, Text):


        functions.MenuAndTitleSelect.ChangeNameDropMenu(self_sales_history, functions.global_variable_self.MenuTypeSalesHistory, "ButtonMenuSearchingSalesHistory", Text)

    
    def ShowDataSalesHistoryController(self, start, end, state):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(SalesHistoryDB.ShowDataSalesHistoryModel, start,end,state)
            return_value = future.result()

            return return_value    