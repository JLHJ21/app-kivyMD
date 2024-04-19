from functools import partial
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty, StringProperty, NumericProperty 
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

from kivymd.uix.label import MDLabel

import intermediary

############
###TABLA

''' Global rv '''
global_rv = global_selectable = None


class TestTable(MDLabel):

   def __init__(self, **kwargs):

        x = StringProperty(None)

        super().__init__(**kwargs)

        '''

        x = lambda x: ModalsDialog.ShowAlertDialog(
                global_selectable,
                "¿Que desea realizar?", 
                "Por favor, elija algunas de las opciones presentadas.", 
                "Cancelar", 
                "Eliminar", 
                "Modificar", 

                lambda x: ModalsDialog.CloseDialog(global_selectable, global_selectable.dialog.dismiss()),
                lambda x: ModalsDialog.ShowAlertDialogDelete
                    (
                        global_selectable,
                        "¿De verdad quiere eliminar este producto?", 
                        "Si es así, adelante",
                        "Cancelar",
                        "Eliminar",
                        lambda x: ModalsDialog.CloseDialog(global_selectable, global_selectable.dialog2.dismiss()),
                        lambda x: print("cerrar")
                    ),
                lambda x: ModalsDialog.ChangePage(global_selectable, "StorePageUpdate", "Almacen - Modificar")
            )
        '''


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True) # ** DIFFERENCE **

class SelectableLabel(RecycleDataViewBehavior, MDFlatButton):


    #row_content = ObjectProperty()

    ''' Add selection support to the Label '''
    index = None
    #selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableLabel, self).__init__(**kwargs) 

        global global_selectable
        global_selectable = self

        #print(self.ids.test)

    def CreateLabels(self):

        #print(SelectableLabel.row_content)

        '''
        self_main = intermediary.global_variable_self

        self_main.root.ids.GridSelectableLabel.add_widget(
                MDLabel(
                    text='how how',
                    halign="center"
                )
            )
        '''

    def refresh_view_attrs(self, rv, index, data):


        #print(global_rv.list_table_data)
    
        ''' Catch and handle the view changes '''
        self.index = index

        #self.ids['id_imagen'].text  = str(index) #if index > 0 else "Imagen"

        #print(global_rv.list_table_labels[0])

        #self.ids[global_rv.list_table_labels[0]].text  = data["dato" + str(index + 1)][index]
        #print(data["dato1"]["nombre"])

        #indexDictionary = RecycleViewTable.StartPagination + 1

        #self.label2_text = data['label2']['text']

        #self.ids['id_nombre'].text = data['dato']['nombre']  # As an alternate method of assignment

        for label, itemData in zip(global_rv.list_table_labels, global_rv.list_table_data):
            
            self.ids[label].text = data['dato'][itemData]
        #    print(label)
        #    print(self.ids[label].text + "  <--- LABEL")
        #    print(data["dato" + str(indexDictionary)][itemData] + "  <--- ITEMDATA")
        #    self.ids[label].text  = data["dato" + str(indexDictionary)][itemData]
            #self.ids['id_proveedor'].text = data['proveedor']['text'] 
            #self.ids['id_cantidad'].text = data['cantidad']['text'] 
            #self.ids['id_precio'].text = data['precio']['text'] 

            #print(str(index) + " <-- index")
            #print(str(label) + " <-- label")
            #print(str(itemData) + " <-- itemData")

        #    indexDictionary += 1
        
        # self.label2_text = data['label2']['text']  # As an alternate method of assignment

        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):

        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
        
    def ButtonDialog(self, x):


        #la variable self de la funcion, se relaciona con la clase RecycleViewTable, no con esta clase SelectableTable
        exec(x)
        
class RecycleViewTable(MDBoxLayout):

    #itemsAmount = ObjectProperty(None)
    
    ''' Variables de los modales Dialogs'''
    
    dialog = dialog2 = dialog3 = None


    list_table_labels = ListProperty([])
    list_table_data = ListProperty([])
    dictionaryPrincipal = ListProperty([])
    modalData = StringProperty(None)
    test = StringProperty(None)

    boleana = True


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


        

        #Llama la función TableData para rellenar los datos de la tabla 
        #Mediante el uso de Clock, ya que __init__ inicia antes de que el .kv exista
        Clock.schedule_once(lambda dt: self.TableData(self.DictionaryDataset))
        Clock.schedule_once(lambda dt: self.CreateLabels(self))
        #Clock.schedule_once(lambda dt: self.Test())

        #self.TableData(self.DictionaryDataset)

    def CreateLabels(self, *args):

        for i in self.list_table_data:

            i = (i).title()

            
            label = MDLabel(
                        text = i,
                        halign="center",
                        font_style = "H6",
                        markup= True
                    )

            self.scroll_box_layout.add_widget(label)
            

    #def Test(self):

    def TableData(self, dictionary):


        if self.boleana:


            exec(self.test)

            #for i in range(1,21): 
            #    d = {f"dato{i}": [f"dato{i}_nombre", f"dato{i}_proveedor", f"dato{i}_cantidad", f"dato{i}_precio"]}

                #for a in self.dictionaryPrincipal:
                #    d['dato{i}'].append(a)

                #Creo indice del diccionario, normalmente se llama dato + numero de iteracion
                #d = {f"dato{i}": []}


                #d[f"dato{i}"].extend(t for t in self.dictionaryPrincipal)


            #    self.DictionaryDataset.update(d)
            
            self.boleana = False


        #print(str(self.list_table_labels) + " | " + str(self.list_table_data) + " | " + str(self.dictionaryPrincipal))

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

            #d = {}

            #IF Statement que permite mostrar la cantidad de items que se visualizaran 
            #Segun la cantidad de items que estimó (el predeterminado es 5)

            if(IterationStartPagination) < self.ItemsAccountPagination:
                

                d = {}
                d['dato'] = {}
                for index, i in enumerate(self.list_table_data):
                    #d[i] = {dictionary[dic][index]}
                    da = { i: dictionary[dic][index]}
                    #da = dictionary[dic][index]
                    #d['dato'] = {i: dictionary[dic][index]}

                    #para LISTA 
                    #d['dato'].append(da)
                    #para Diccionario
                    d['dato'].update(da)
            
                i = {'on_release': partial(SelectableLabel.ButtonDialog, self, self.modalData)}
                d.update(i)

                #Agregar a la tabla los items
                self.rv.data.append(d)


                #print(str(items['nombre']) + " items")
                #CICLO FOR AQUI OJO
                #Diccionario que almacena los datos que se mostrarán en la tabla
                #d[items] = {dictionary[dic][index]}


                #d = {
                #    items: {'text': dictionary[dic][index]}, 
                    #se llama a la funcion ButtonDialog de la clase SelectableLabel con partial
                    #self es el primer parametro
                    # y boton + dic, el segundo parametro
                    #s'on_release': partial(SelectableLabel.ButtonDialog, self, self.modalData)
                #}


                
                
                #Suma el valor a la paginacion
                IterationStartPagination += 1  

            else:
                #Si el comienzo y el final de la paginacion son iguales o mayores, se rompe el ciclo FOR
                break

        #print(self.DictionaryDataset)


    
    
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
        SelectableLabel.CreateLabels(self)
        typeDialog

    def ChangeItemsAmount(self):

        RecycleViewTable.StartPagination = 0

        #Switch que cambia la cantidad de items a mostrar segun la cantidad que tenia previamente
        match RecycleViewTable.ItemsAccountPagination:
            case 5:
                RecycleViewTable.ItemsAccountPagination = RecycleViewTable.StaticItemsAccountPagination = 10
            case 10:
                RecycleViewTable.ItemsAccountPagination = RecycleViewTable.StaticItemsAccountPagination = 15
            case 15:
                RecycleViewTable.ItemsAccountPagination = RecycleViewTable.StaticItemsAccountPagination = 5
            case _:
                RecycleViewTable.ItemsAccountPagination = RecycleViewTable.StaticItemsAccountPagination = 5

        

        #Cambia el texto del boton ItemsAmount
        global_rv.ids.ItemsAmount.text = "Items por página: " + str(global_rv.ItemsAccountPagination)

        self.StatusButtonPagination("both")
        #Llama la función TableData para rellenar los datos de la tabla
        global_rv.TableData(global_rv.DictionaryDataset)

    def ChangeItemsAmountButtons(self, button):
        

        #Asignacion del nuevo valor del inicio de la paginacion, (primera variable, primer número 'Mostrando AQUI - X)
        #Asignacion del nuevo valor de los items mostrados del diccionario (segunda variable, segundo número 'Mostrando X - AQUI)
        match button:
                
            case "left":

                #RESTA
                RecycleViewTable.StartPagination = RecycleViewTable.StartPagination - RecycleViewTable.StaticItemsAccountPagination
                RecycleViewTable.ItemsAccountPagination = RecycleViewTable.ItemsAccountPagination - RecycleViewTable.StaticItemsAccountPagination

                self.StatusButtonPagination("left")

                
            case "right":

                #SUMA
                RecycleViewTable.StartPagination = RecycleViewTable.StartPagination  + RecycleViewTable.StaticItemsAccountPagination
                RecycleViewTable.ItemsAccountPagination = RecycleViewTable.ItemsAccountPagination + RecycleViewTable.StaticItemsAccountPagination

                self.StatusButtonPagination("right")
                
                
            case _:
                RecycleViewTable.StartPagination = 0
                RecycleViewTable.ItemsAccountPagination = 5

        global_rv.TableData(global_rv.DictionaryDataset)

    def StatusButtonPagination(self, side):

        match side:
            case "left":

                #Activa el boton de la derecha de la paginacion
                global_rv.ids.ButtonRightPagination.disabled = False

                #IF Statement, si el inicio de la paginación es 0 DISABLED es True desactivando el boton izquierdo 
                #caso contrario DISABLED es False activando el boton 
                if global_rv.StartPagination <= 0:
                    #Desactiva boton izquierdo
                    global_rv.ids.ButtonLeftPagination.disabled = True 

                else:
                    #Activa boton izquierdo
                    global_rv.ids.ButtonLeftPagination.disabled = False

                #global_rv.ButtonLeftPagination.disabled = True if global_rv.StartPagination <= 0 else False 
            case "right":

                #Activa el boton de la izquierda de la paginacion
                global_rv.ids.ButtonLeftPagination.disabled = False

                #IF Statement, si la cantidad de items de la paginación es mayor a los items del diccionario
                #el DISABLED sera True, en caso contrario será False
                if global_rv.ItemsAccountPagination >= len(global_rv.DictionaryDataset):

                    #Asigna la cantidad máxima de items del diccionario
                    #global_rv.ItemsAccountPagination = len(global_rv.DictionaryDataset)

                    #Desactiva boton derecho
                    global_rv.ids.ButtonRightPagination.disabled = True

                else: 
                    #Activa boton derecho
                    global_rv.ids.ButtonRightPagination.disabled = False

            case "both":

                #left

                #IF Statement, si el inicio de la paginación es 0 DISABLED es True desactivando el boton izquierdo 
                #caso contrario DISABLED es False activando el boton 
                if RecycleViewTable.StartPagination <= 0:
                    #Desactiva boton izquierdo
                    global_rv.ids.ButtonLeftPagination.disabled = True 

                else:
                    #Activa boton izquierdo
                    global_rv.ids.ButtonLeftPagination.disabled = False

                #right

                #IF Statement, si la cantidad de items de la paginación es mayor a los items del diccionario
                #el DISABLED sera True, en caso contrario será False
                if RecycleViewTable.ItemsAccountPagination >= len(RecycleViewTable.DictionaryDataset):

                    #Asigna la cantidad máxima de items del diccionario
                    #global_rv.ItemsAccountPagination = len(global_rv.DictionaryDataset)

                    #Desactiva boton derecho
                    global_rv.ids.ButtonRightPagination.disabled = True

                else: 
                    #Activa boton derecho
                    global_rv.ids.ButtonRightPagination.disabled = False
            case _:
                pass


############
