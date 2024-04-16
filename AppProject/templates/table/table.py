from functools import partial
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton


from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior


from kivy.uix.recycleview import RecycleView

import intermediary

############
###TABLA

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True) # ** DIFFERENCE **

''' Global rv '''
global_rv = global_selectable = None


class SelectableLabel(RecycleDataViewBehavior, MDFlatButton):

    ''' Add selection support to the Label '''
    index = None
    #selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    cols = 5

    def refresh_view_attrs(self, rv, index, data):

    
        ''' Catch and handle the view changes '''
        self.index = index

        #self.ids['id_imagen'].text  = str(index) #if index > 0 else "Imagen"
        self.ids['id_nombre'].text  = data['nombre']['text']
        self.ids['id_proveedor'].text = data['proveedor']['text'] 
        self.ids['id_cantidad'].text = data['cantidad']['text'] 
        self.ids['id_precio'].text = data['precio']['text'] 

        
        # self.label2_text = data['label2']['text']  # As an alternate method of assignment

        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        global global_selectable
        global_selectable = self

        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
        
    def ButtonDialog(self, x):

        #la variable self de la funcion, se relaciona con la clase RecycleViewTable, no con esta clase SelectableTable

        ModalsDialog.ShowAlertDialog(
            self,
            "¿Que desea realizar?", 
            "Por favor, elija algunas de las opciones presentadas.", 
            "Cancelar", 
            "Eliminar", 
            "Modificar", 

            lambda x: ModalsDialog.CloseDialog(self, self.dialog.dismiss()),
            lambda x: ModalsDialog.ShowAlertDialogDelete
                (
                    self,
                    "¿De verdad quiere eliminar este producto?", 
                    "Si es así, adelante",
                    "Cancelar",
                    "Eliminar",
                    lambda x: ModalsDialog.CloseDialog(self, self.dialog2.dismiss()),
                    lambda x: print("cerrar")
                ),
            lambda x: ModalsDialog.ChangePage(self, "StorePageUpdate", "Almacen - Modificar")
        )


        print('button', x, 'pressed')
        
        
class RecycleViewTable(MDBoxLayout):

    #itemsAmount = ObjectProperty(None)
    
    ''' Variables de los modales Dialogs'''
    
    dialog = None
    dialog2 = None
    dialog3 = None


    #Cantidad de items que se mostrará en el RecycleView
    StartPagination = 0
    ItemsAccountPagination = 5

    #Variable estaticas que permiten, el uso de los botones para la paginación
    StaticStartPagination = StartPagination
    StaticItemsAccountPagination = ItemsAccountPagination

    #Diccionario donde se almacenaran los datos
    DictionaryDataset = {}

    def __init__(self, **kwargs):
        super(RecycleViewTable, self).__init__(**kwargs)

        global global_rv
        global_rv = self
        
        #Texto de la cantidad de items que se muestran
        #self.ids.ItemsAmount.text = "Items por página: " + str(self.ItemsAccountPagination)
        
        #dictionary donde estará todos los datos de la tabla

        for i in range(1,21):

            d = {f"dato{i}": [f"dato{i}_nombre", f"dato{i}_proveedor", f"dato{i}_cantidad", f"dato{i}_precio",]}

            #for a in self.dictionaryPrincipal:
            #    d['dato{i}'].append(a)

            #Creo indice del diccionario, normalmente se llama dato + numero de iteracion
            #d = {f"dato{i}": []}

    
            #d[f"dato{i}"].extend(t for t in self.dictionaryPrincipal)


            self.DictionaryDataset.update(d)

        #Llama la función TableData para rellenar los datos de la tabla 
        #Mediante el uso de Clock, ya que __init__ inicia antes de que el .kv exista
        Clock.schedule_once(lambda dt: self.TableData(self.DictionaryDataset))
        #self.TableData(self.DictionaryDataset)


    def TableData(self, dictionary):

        #Cuenta la cantidad de items que tiene el diccionario
        CountDictionary = len(dictionary)

        #Cambia el texto del Label ShowItems, a los que haya en el diccionario
        #Si el valor es 0, le suma un 1 solo visualmente
        if self.StartPagination <= 0:
            self.ids.ItemsShowed.text = f" Mostrando {str(self.StartPagination + 1)}-{str(self.ItemsAccountPagination)} de {str(CountDictionary)}"

        #Muestra el valor de StartPagination normalmente, sin la suma del 1
        else:
            self.ids.ItemsShowed.text = f" Mostrando {str(self.StartPagination)}-{str(self.ItemsAccountPagination)} de {str(CountDictionary)}"

        #Declaración de la variable donde irá los items y se mostrarán en la tabla
        self.rv.data = []

        #Donde comienza la variable
        IterationStartPagination = self.StartPagination

        #Asignando una variable donde calcula desde donde se comenzará la paginación de los items que se iteraran en el ciclo FOR
        IterationItems = list(dictionary)[self.StartPagination:]

        #FOR al diccionario que contiene los datos de la base de datos
        for dic in IterationItems: 

            #IF Statement que permite mostrar la cantidad de items que se visualizaran 
            #Segun la cantidad de items que estimó (el predeterminado es 5)
            if(IterationStartPagination) < self.ItemsAccountPagination:

                #Diccionario que almacena los datos que se mostrarán en la tabla
                d = {
                        'nombre': {'text': dictionary[dic][0]}, 
                        'proveedor': {'text': dictionary[dic][1]},
                        'cantidad': {'text': dictionary[dic][2]},
                        'precio': {'text': dictionary[dic][3]},
                        #se llama a la funcion ButtonDialog de la clase SelectableLabel con partial
                        #self es el primer parametro
                        # y boton + dic, el segundo parametro
                        'on_release': partial(SelectableLabel.ButtonDialog, self, 'boton' + dic)
                    }
                
                #Agregar a la tabla los items
                self.rv.data.append(d)
                
                #Suma el valor a la paginacion
                IterationStartPagination += 1  
            else:
                #Si el comienzo y el final de la paginacion son iguales o mayores, se rompe el ciclo FOR
                break        

    
    
class ModalsDialog():
    ############
    ###MODALES

    ## CALLBACK PARA CAMBIAR DE PAGINA CON MDTopAppBar BUTTON
    def ChangePage(self, page, text):

        self_main = intermediary.global_variable_self
        self_main.root.ids.screen_manager.current = page
        self_main.root.ids.toolbar.title = text

        ModalsDialog.CloseDialog(self, self.dialog.dismiss())
        

    def ShowAlertDialog(self, title, text, optionOne, optionTwo, optionThree, releaseOne, releaseTwo, releaseThree):
        
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text= text,
                buttons=[
                    MDFlatButton(
                        text=optionOne,
                        #text_color=self.theme_cls.primary_color,
                        on_press = releaseOne
                    ),
                    MDRaisedButton(
                        text=optionTwo,
                        md_bg_color="red",
                        text_color="white",
                        on_press = releaseTwo
                    ),
                    MDRaisedButton(
                        text=optionThree,
                        md_bg_color="orange",
                        on_release= releaseThree
                                                        
                    ),
                ],
            )
        self.dialog.open()

    def ShowAlertDialogDelete(self, title, text, textButtonOne, textButtonTwo, releaseButtonOne, releaseButtonTwo):

        ModalsDialog.CloseDialog(self.dialog.dismiss())
        
        if not self.dialog2:
            self.dialog2 = MDDialog(
                title=title,
                text=text,
                buttons=[
                    MDFlatButton(
                        text=textButtonOne,
                        text_color= "red",
                        on_release = releaseButtonOne
                    ),
                    MDRaisedButton(
                        text=textButtonTwo,
                        text_color="white",
                        md_bg_color="red",
                        on_release = releaseButtonTwo
                    ),
                ],
            )
        self.dialog2.open()
    
    
    def CloseDialog(self, typeDialog):

        #Funcion dinamica para cerrar los dialogs
        typeDialog

    def ChangeItemsAmount(self):

        self.StartPagination = 0

        #Switch que cambia la cantidad de items a mostrar segun la cantidad que tenia previamente
        match self.ItemsAccountPagination:
            case 5:
                self.ItemsAccountPagination = self.StaticItemsAccountPagination = 10
            case 10:
                self.ItemsAccountPagination = self.StaticItemsAccountPagination = 15
            case 15:
                self.ItemsAccountPagination = self.StaticItemsAccountPagination = 5
            case _:
                self.ItemsAccountPagination = self.StaticItemsAccountPagination = 5

        

        #Cambia el texto del boton ItemsAmount
        self.ids.ItemsAmount.text = "Items por página: " + str(self.ItemsAccountPagination)

        self.StatusButtonPagination("both")
        #Llama la función TableData para rellenar los datos de la tabla
        self.TableData(self.DictionaryDataset)

    def ChangeItemsAmountButtons(self, button):


        #Asignacion del nuevo valor del inicio de la paginacion, (primera variable, primer número 'Mostrando AQUI - X)
        #Asignacion del nuevo valor de los items mostrados del diccionario (segunda variable, segundo número 'Mostrando X - AQUI)
        match button:
                
            case "left":

                #RESTA
                self.StartPagination = self.StartPagination - self.StaticItemsAccountPagination
                self.ItemsAccountPagination = self.ItemsAccountPagination - self.StaticItemsAccountPagination

                self.StatusButtonPagination("left")

                
            case "right":

                #SUMA
                self.StartPagination = self.StartPagination  + self.StaticItemsAccountPagination
                self.ItemsAccountPagination = self.ItemsAccountPagination + self.StaticItemsAccountPagination

                self.StatusButtonPagination("right")
                
                
            case _:
                self.StartPagination = 0
                self.ItemsAccountPagination = 5

        self.TableData(self.DictionaryDataset)

    def StatusButtonPagination(self, side):

        match side:
            case "left":

                #Activa el boton de la derecha de la paginacion
                self.ids.ButtonRightPagination.disabled = False

                #IF Statement, si el inicio de la paginación es 0 DISABLED es True desactivando el boton izquierdo 
                #caso contrario DISABLED es False activando el boton 
                if self.StartPagination <= 0:
                    #Desactiva boton izquierdo
                    self.ids.ButtonLeftPagination.disabled = True 

                else:
                    #Activa boton izquierdo
                    self.ids.ButtonLeftPagination.disabled = False

                #self.ButtonLeftPagination.disabled = True if self.StartPagination <= 0 else False 
            case "right":

                #Activa el boton de la izquierda de la paginacion
                self.ids.ButtonLeftPagination.disabled = False

                #IF Statement, si la cantidad de items de la paginación es mayor a los items del diccionario
                #el DISABLED sera True, en caso contrario será False
                if self.ItemsAccountPagination >= len(self.DictionaryDataset):

                    #Asigna la cantidad máxima de items del diccionario
                    #self.ItemsAccountPagination = len(self.DictionaryDataset)

                    #Desactiva boton derecho
                    self.ids.ButtonRightPagination.disabled = True

                else: 
                    #Activa boton derecho
                    self.ids.ButtonRightPagination.disabled = False

            case "both":

                #left

                #IF Statement, si el inicio de la paginación es 0 DISABLED es True desactivando el boton izquierdo 
                #caso contrario DISABLED es False activando el boton 
                if self.StartPagination <= 0:
                    #Desactiva boton izquierdo
                    self.ids.ButtonLeftPagination.disabled = True 

                else:
                    #Activa boton izquierdo
                    self.ids.ButtonLeftPagination.disabled = False

                #right

                #IF Statement, si la cantidad de items de la paginación es mayor a los items del diccionario
                #el DISABLED sera True, en caso contrario será False
                if self.ItemsAccountPagination >= len(self.DictionaryDataset):

                    #Asigna la cantidad máxima de items del diccionario
                    #self.ItemsAccountPagination = len(self.DictionaryDataset)

                    #Desactiva boton derecho
                    self.ids.ButtonRightPagination.disabled = True

                else: 
                    #Activa boton derecho
                    self.ids.ButtonRightPagination.disabled = False
            case _:
                pass


############
