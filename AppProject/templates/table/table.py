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
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.core.text import Label as CoreLabel
from kivy.core.text.markup import MarkupLabel

from kivy.uix.recycleview import RecycleView

from kivymd.uix.label import MDLabel
from kivy.uix.label import Label

from kivy.factory import Factory
from kivy.uix.image import Image

import intermediary
import weakref
from retry import retry

############
###TABLA

''' Global rv '''
global_selectable = global_gridSelectableLabelChildren = global_id_table = global_columnas  = global_need_image = None

global_labels_order = have_labels_cols = global_need_image = False

global_dictionary = []

global_rv = {}

global_dictionary_table_data = {}

        


class ContentCashierPage(MDBoxLayout):
    pass

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True) # ** DIFFERENCE **

class SelectableLabel(RecycleDataViewBehavior, MDFlatButton):


    gridSelectableLabel = ObjectProperty(None)
    objectTest = ObjectProperty(None)

    #row_content = ObjectProperty()

    ''' Add selection support to the Label '''
    index = None
    #selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SelectableLabel, self).__init__(**kwargs) 

        #global que permite usar el self de SelectableLabel en otras clases
        global global_selectable
        global_selectable = self

        

        #self.CreateLabelsWidgets()
    
    #Columnas de las tablas y el nombre que tendrán
    def CreateLabelsWidgets(self, dictionary, need_image):        

        #se agrega al mdgridlayout para que se muestre
        #self.gridSelectableLabel.add_widget(label)           

        #self.gridSelectableLabel.ids["id_" + str(i)] = weakref.ref(label)
            
        #print(str(RecycleViewTable.list_table_data) + " <--- list table data")
        
        if (self == None):
            #Clock.schedule_once(lambda dt: RecycleViewTable.CreateLabels(global_rv))
            
            pass
        else:


            #RecycleViewTable.GetValueFromKivy(global_rv.objecto)
            
            #print(global_dictionary_table_data)


            self.children[0].cols = global_columnas


            #print(self.ids['GridSelectableLabel'].children)


            #NOMBRE DEL ID = OBJETO QUE SE LE AGREGARA ESO
            #self.ids[global_id_table] = weakref.ref(self.children[0])
            
            #self.scroll_box_layout.add_widget(label)           
            
            for index, p in enumerate(dictionary): 


                if index == 0 :

                    if need_image:

                        l=Image(
                            source= "",
                            fit_mode= "scale-down",
                            size_hint= [1, 1],
                        )

                    else:

                        l=MDLabel(
                            text=str(p) + str(index),
                            halign="center",
                            font_style = "H6",
                            markup= True,
                        )


                    id_label = "id_" + str(p)

                    self.ids.GridSelectableLabel.add_widget(l)
                    self.ids.GridSelectableLabel.ids[id_label] = weakref.ref(l)

                else:
                    
                    l=MDLabel(
                        text=str(p) + str(index),
                        halign="center",
                        font_style = "H6",
                        #font_size= ,
                        markup= True,
                        #is_image=False
                    )

                    id_label = "id_" + str(p)
                    
                    self.ids.GridSelectableLabel.add_widget(l)
                    self.ids.GridSelectableLabel.ids[id_label] = weakref.ref(l)

            
    def refresh_view_attrs(self, rv, index, data):

        global have_labels_cols
        global global_gridSelectableLabelChildren
        #global global_dictionary

        #print(global_rv.objecto.id_table)
        #print(global_dictionary_table_data[global_rv.objecto.id_table])

        for i in global_rv:

            #print(str(global_rv[i].objecto.rv) + " GLOBAL RV")        

            if global_rv[i].objecto.rv == rv:
                
                self_objecto_tabla = global_rv[i].objecto

                # RecycleViewTable.GetValueFromKivy(global_rv.objecto)

                #print(global_rv[i].objecto.list_table_data)
                #for i in global_rv[i].objecto.list_table_data:
                #    global_dictionary = []
                #    global_dictionary.append(i)


                #print(self_objecto_tabla.list_table_labels[::-1])

            #(str(rv) + " <--- RV")
        
        try:
            if self.gridSelectableLabel.children[0]:
                pass

        except IndexError:

            #MUY IMPORTANTE OJO, PERMITE QUE SE PUEDA PASAR EL VALOR DEL SELF DE CADA OBJECTO INDIVIDUAL AL SELECTABLE LABEL
            self.CreateLabelsWidgets(self_objecto_tabla.list_table_labels, self_objecto_tabla.need_image)

        #print(str(global_rv['tableCajeroProducto'].objecto.list_table_data) + " refresh")        

        ''' Catch and handle the view changes '''

        #print(global_rv.objecto.list_table_data)


        #print(str(global_rv[rv]['tableCajeroProducto']) + "refresh")

        #print(str(global_rv))        


        
            


        self.index = index
        #self.ids["a"] = weakref.ref(self.gridSelectableLabel.parent)


        #OJO
        #print(self.ids.a.children[0])
        #print(self.ids.a.ids.GridSelectableLabel.children)


        #ciclo FOR que agrega los datos en la tabla segun lo escrito en el .kv
        #Une las listas de list_table_labels y list_table_data con el zip, para que la iteracion sea 0:0 1:1
        
        for index, (label, itemData) in enumerate(zip(self_objecto_tabla.list_table_labels[::-1], self_objecto_tabla.list_table_data[::-1])):

            #print(str(len(global_rv.list_table_labels)) + " len")
            
            #print(self.ids.GridSelectableLabel.children)

            #print(global_rv.list_table_data[::-1])


            try:
                
                print(str(self.gridSelectableLabel.children[index].source) + " <--- SOURCE")

                self.gridSelectableLabel.children[index].source = data['dato'][itemData]
                
            except AttributeError:
                #print(str(self.gridSelectableLabel.children[index].text) + " <--- TEXT")

                self.gridSelectableLabel.children[index].text = data['dato'][itemData]
                
        

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
    
    ''' Variables de los modales Dialogs'''
    
    dialog = dialog2 = dialog3  =  dialogShowUpdate = None


    list_table_labels = ListProperty([])
    list_table_data = ListProperty([])
    #dictionaryPrincipal = ListProperty([])
    modalData = StringProperty(None)
    test = StringProperty(None)
    columnas = NumericProperty(1)
    id_table = StringProperty(None)
    objecto = ObjectProperty(None)
    need_image = BooleanProperty(True)
    boleana = True

    #Cantidad de items que se mostrará en el RecycleView
    StartPagination = 0
    ItemsAccountPagination = 5

    #Variable estaticas que permiten, el uso de los botones para la paginación
    StaticStartPagination = StartPagination
    StaticItemsAccountPagination = ItemsAccountPagination

    #Diccionario donde se almacenaran los datos
    DictionaryDataset = {}

    def GetValueFromKivy(variable):
        
        value = variable
        
        return value

    def __init__(self, **kwargs):
        super(RecycleViewTable, self).__init__(**kwargs)
     
        #Window.bind(on_resize=self.on_window_resize)

        #Mediante el uso de Clock, ya que __init__ inicia antes de que el .kv exista
        #Clock.schedule_once(lambda dt: SelectableLabel.CreateLabelsWidgets(global_selectable))


        Clock.schedule_once(lambda dt: self.CreateLabels(self))
        #Clock.schedule_once(lambda dt: self.on_window_resize)
        Clock.schedule_once(lambda dt: self.TableData(self.objecto.DictionaryDataset))
        #Clock.schedule_once(lambda dt: self.Test())

        #self.TableData(self.DictionaryDataset)

    '''
    def on_window_resize(self, instance, width, height):
        font_size_height = int(height / 10)
        font_size_width = int(width / 45)

        font_size = min(font_size_height, font_size_width)
        #self.ids.labeltest.font_size = dp(font_size)
        
        for widget in self.walk():
            if hasattr(widget, 'font_size'):
                widget.font_size = dp(font_size)
    '''

    #TITULO
    def CreateLabels(self, *args):



        global global_id_table, global_columnas, global_dictionary_table_data, global_need_image


        global_need_image = self.objecto.need_image


        global global_rv


        item = {self.objecto.rv: self}
        #global_rv[self.objecto.rv] = {}
        global_rv.update(item)
        
        global_id_table = self.objecto.id_table

        global_dictionary_table_data[self.objecto.id_table] = []




        lista = self.objecto.list_table_labels

        global_dictionary_table_data[self.objecto.id_table].append(lista)


        #print(global_dictionary_table_data)
        


        #print(self.list_table_data)


        #NOMBRE DEL ID = OBJETO QUE SE LE AGREGARA ESO
        #self.ids[self.id_table] = weakref.ref(self)

        #print(self.ids.hello)

        #global global_dictionary

        #global_dictionary = []

        #Permite eliegir el numero de columnas dinamicamente
        self.objecto.children[2].children[0].cols = self.objecto.columnas

        global_columnas = self.objecto.columnas

        font_size = int(self.width/11 if self.width/11 > 10 else self.width/7)

        #Crea las cabeceras de la tabla
        for index, i in enumerate(self.objecto.list_table_data):



            #Capitaliza el inicio de la palabra
            i = (i).title()

            #Caracteristicas que tendrá el widget, en este caso un MDLabel
            label = MDLabel(
                    #text = "[size="+ str(font_size) +"]"+str(i)+"[/size]",
                    text = i,
                    halign="center",
                    font_style = "H6",
                    #font_size= ,
                    markup= True,
                )

            #se agrega al mdgridlayout para que se muestre
            self.objecto.scroll_box_layout.add_widget(label)

            '''
            if index == 0:
                #print(i)

                if self.objecto.need_image == False:
                    #print(' imagen no es necesitada')
                    pass
                pass
            else:

                print(i)

                #Capitaliza el inicio de la palabra
                i = (i).title()

                #Caracteristicas que tendrá el widget, en este caso un MDLabel
                label = MDLabel(
                        #text = "[size="+ str(font_size) +"]"+str(i)+"[/size]",
                        text = i,
                        halign="center",
                        font_style = "H6",
                        #font_size= ,
                        markup= True,
                    )

                #se agrega al mdgridlayout para que se muestre
                self.objecto.scroll_box_layout.add_widget(label)           
            '''
        #for i in self.objecto.list_table_data:
        #    global_dictionary.append(i)


    def TableData(self, dictionary):

        if self.objecto.boleana:

            self.objecto.DictionaryDataset = {}

            #ejecuta lo escrito en el kv, normalmente es donde se ejecutará el codigo mongodb que nos dará los datos de la base de datos
            exec(self.objecto.test)

            dictionary = self.objecto.DictionaryDataset

            #self.objecto.dictionary = self.objecto.DictionaryDataset
            
            #permite que se active solamente una vez
            self.objecto.boleana = False

            ModalsDialog.StatusButtonPagination('self', self.objecto.rv, "both")
            
        ##################################################################

        #Cuenta la cantidad de items que tiene el diccionario
        CountDictionary = len(dictionary)
        #print(CountDictionary)

        #Cambia el texto del Label ShowItems, a los que haya en el diccionario
        #Si el valor es 0, le suma un 1 solo visualmente
        if self.objecto.StartPagination <= 0:
            self.objecto.ids.ItemsShowed.text = f" Mostrando {str(self.objecto.StartPagination + 1)}-{str(self.objecto.ItemsAccountPagination)} de {str(CountDictionary)}"

        #Muestra el valor de StartPagination normalmente, sin la suma del 1
        else:
            self.objecto.ids.ItemsShowed.text = f" Mostrando {str(self.objecto.StartPagination)}-{str(self.objecto.ItemsAccountPagination)} de {str(CountDictionary)}"

        #Declaración de la variable donde irá los items y se mostrarán en la tabla
        self.objecto.rv.data = []

        #Donde comienza la variable
        IterationStartPagination = self.objecto.StartPagination

        #Asignando una variable donde calcula desde donde se comenzará la paginación de los items que se iteraran en el ciclo FOR
        IterationItems = list(dictionary)[self.objecto.StartPagination:]


        #FOR al diccionario que contiene los datos de la base de datos
        for dic in IterationItems: 

            #d = {}

            #IF Statement que permite mostrar la cantidad de items que se visualizaran 
            #Segun la cantidad de items que estimó (el predeterminado es 5)

            if(IterationStartPagination) < self.objecto.ItemsAccountPagination:
                
                #crea el diccionario donde se almacenará la información que será enviada al SelectableLabel
                d = {}
                #Crear un nuevo diccionario donde se agregará
                d['dato'] = {}
                for index, i in enumerate(self.objecto.list_table_data):
                    
                    #crea diccionario con los datos dentro del diccionario, segun los datos escritos en el kivy haciendo lo siguiente en el diccionario,
                    # {nombre_del_dato, diccionario[datos_que_se_mostraran], indice[posicion_del_dato]}


                    da = { i: dictionary[dic][index]}

                    #agrega los datos al diccionario principal
                    d['dato'].update(da)
                    

            
                #crea diccionario el on_release al diccionario principal
                i = {'on_release': partial(SelectableLabel.ButtonDialog, self.objecto, self.objecto.modalData)}
                #agrega el on_release
                d.update(i)

                #dictionary donde estará todos los datos de la tabla
                #Agregar a la tabla los items, activando el selectableLabel y crean un label para cada uno
                self.objecto.rv.data.append(d)

                #Suma el valor a la paginacion
                IterationStartPagination += 1  

            else:
                #Si el comienzo y el final de la paginacion son iguales o mayores, se rompe el ciclo FOR
                break

class ModalsDialog():

    ############
    ###MODALES

    ## CALLBACK PARA CAMBIAR DE PAGINA
    def ChangePage(self, page, text):

        #obtiene el self principal del kivy
        self_main = intermediary.global_variable_self
        #cambia segun la pagina querida
        self_main.root.ids.screen_manager.current = page
        #cambia el titulo del menu de arriba segun el nombre que queramos
        self_main.root.ids.toolbar.title = text

        #Cierra los modales activados
        ModalsDialog.CloseDialog('self', RecycleViewTable.dialog.dismiss())
        
    #Modal 1
    def ShowAlertDialog(self, title, text, optionOne, optionTwo, optionThree, releaseOne, releaseTwo, releaseThree):
 
        #Si no existe, normalmente no, lo crea
        #if not RecycleViewTable.dialog:
        #Caracteristicas
        RecycleViewTable.dialog = MDDialog(
            title=title,
            text= text,
            buttons=[
                #Boton de Cancelar
                MDFlatButton(
                    text=optionOne,
                    #text_color=self.theme_cls.primary_color,
                    on_press = releaseOne
                ),
                #Boton de modificar o algun otro uso
                MDRaisedButton(
                    text=optionTwo,
                    md_bg_color="red",
                    text_color="white",
                    on_press = releaseTwo
                ),
                #Boton de Aceptar
                MDRaisedButton(
                    text=optionThree,
                    md_bg_color="orange",
                    on_release= releaseThree
                                                    
                ),
            ],
        )
        #Abre el modal
        RecycleViewTable.dialog.open()

    def ChangeAmountProductModal(self, title):

        ModalsDialog.CloseDialog("self", RecycleViewTable.dialog.dismiss())

        dialogShowUpdate = MDDialog(
            title=title,
            type="custom",
            content_cls=ContentCashierPage(),
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    md_bg_color="red",
                    text_color="white",
                ),
                MDRaisedButton(
                    text="Aceptar",
                    md_bg_color="blue",
                    #text_color=self.theme_cls.primary_color,
                ),
            ],
        )
        dialogShowUpdate.open()

    def ShowUpdateDataModal(self, title, text, optionOne, optionTwo, optionThree, releaseOne, releaseTwo, releaseThree):
 
        #Si no existe, normalmente no, lo crea
        #if not RecycleViewTable.dialog:
        #Caracteristicas
        RecycleViewTable.dialogShowUpdate = MDDialog(
            title=title,
            text= text,
            buttons=[
                #Boton de Cancelar
                MDFlatButton(
                    text=optionOne,
                    #text_color=self.theme_cls.primary_color,
                    on_press = releaseOne
                ),
                #Boton de modificar o algun otro uso
                MDRaisedButton(
                    text=optionTwo,
                    md_bg_color="red",
                    text_color="white",
                    on_press = releaseTwo
                ),
                #Boton de Aceptar
                MDRaisedButton(
                    text=optionThree,
                    md_bg_color="orange",
                    on_release= releaseThree
                                                    
                ),
            ],
        )
        #Abre el modal
        RecycleViewTable.dialogShowUpdate.open()
        

    def ShowAlertDialogDelete(self, title, text, textButtonOne, textButtonTwo, releaseButtonOne, releaseButtonTwo):

        #Cierra el modal 1
        ModalsDialog.CloseDialog('self',RecycleViewTable.dialog.dismiss())
        
        #Si no existe, normalmente no, lo crea
        #if not RecycleViewTable.dialog2:
        RecycleViewTable.dialog2 = MDDialog(
            title=title,
            text=text,
            buttons=[
                #Boton de Cancelar
                MDFlatButton(
                    text=textButtonOne,
                    text_color= "red",
                    on_release = releaseButtonOne
                ),
                #Boton de Aceptar
                MDRaisedButton(
                    text=textButtonTwo,
                    text_color="white",
                    md_bg_color="red",
                    on_release = releaseButtonTwo
                ),
            ],
        )

        #Abre el modal
        RecycleViewTable.dialog2.open()
    
    
    def CloseDialog(self, typeDialog):

        #Funcion dinamica para cerrar los dialogs
        #RecycleViewTable.CreateLabels(self)
        #print(RecycleViewTable.dialog)
        typeDialog

    def ChangeItemsAmount(self, rv):

        #Reinicia la variable a 0
        global_rv[rv].objecto.StartPagination = 0

        #Switch que cambia la cantidad de items a mostrar segun la cantidad que tenia previamente
        match global_rv[rv].objecto.ItemsAccountPagination:
            case 5:
                global_rv[rv].objecto.ItemsAccountPagination = global_rv[rv].objecto.StaticItemsAccountPagination = 10
            case 10:
                global_rv[rv].objecto.ItemsAccountPagination = global_rv[rv].objecto.StaticItemsAccountPagination = 15
            case 15:
                global_rv[rv].objecto.ItemsAccountPagination = global_rv[rv].objecto.StaticItemsAccountPagination = 5
            case _:
                global_rv[rv].objecto.ItemsAccountPagination = global_rv[rv].objecto.StaticItemsAccountPagination = 5

        

        #Cambia el texto del boton ItemsAmount

        global_rv[rv].objecto.ids.ItemsAmount.text = "Items por página: " + str(global_rv[rv].objecto.ItemsAccountPagination)

        #Llama la funcion para ver si ambas flechas se desactivan al actualizar los datos
        self.StatusButtonPagination(rv, "both")
        #Llama la función TableData para rellenar los datos de la tabla

        #print()
        #print(global_rv[rv].objecto.DictionaryDataset)

        global_rv[rv].objecto.TableData(global_rv[rv].objecto.DictionaryDataset)
        #print(rv)

    def ChangeItemsAmountButtons(self, rv, button):

        #Asignacion del nuevo valor del inicio de la paginacion, (primera variable, primer número 'Mostrando AQUI - X)
        #Asignacion del nuevo valor de los items mostrados del diccionario (segunda variable, segundo número 'Mostrando X - AQUI)
        match button:
                
            case "left":

                #RESTA
                global_rv[rv].objecto.StartPagination = global_rv[rv].objecto.StartPagination - global_rv[rv].objecto.StaticItemsAccountPagination
                global_rv[rv].objecto.ItemsAccountPagination = global_rv[rv].objecto.ItemsAccountPagination - global_rv[rv].objecto.StaticItemsAccountPagination

                #Llama la funcion para ver si se desactiva la flecha izquierda
                self.StatusButtonPagination(rv, "left")

                
            case "right":

                #SUMA
                global_rv[rv].objecto.StartPagination = global_rv[rv].objecto.StartPagination  + global_rv[rv].objecto.StaticItemsAccountPagination
                global_rv[rv].objecto.ItemsAccountPagination = global_rv[rv].objecto.ItemsAccountPagination + global_rv[rv].objecto.StaticItemsAccountPagination

                #Llama la funcion para ver si se desactiva la flecha derecha
                self.StatusButtonPagination(rv, "right")
                
                
            case _:
                global_rv[rv].objecto.StartPagination = 0
                global_rv[rv].objecto.ItemsAccountPagination = 5

        #Llama a esta funcion para actualizar los datos
        global_rv[rv].objecto.TableData(global_rv[rv].objecto.DictionaryDataset)

    #Funcion que sirva para activar o desactivar las flechas de la paginacion en caso tal que no haya más objetos a mostrar
    def StatusButtonPagination(self, rv, side):

        match side:
            #Flecha de la izquierda
            case "left":

                #Activa el boton de la derecha de la paginacion
                global_rv[rv].objecto.ids.ButtonRightPagination.disabled = False

                #IF Statement, si el inicio de la paginación es 0 DISABLED es True desactivando el boton izquierdo 
                #caso contrario DISABLED es False activando el boton 
                if global_rv[rv].objecto.StartPagination <= 0:
                    #Desactiva boton izquierdo
                    global_rv[rv].objecto.ids.ButtonLeftPagination.disabled = True 

                else:
                    #Activa boton izquierdo
                    global_rv[rv].objecto.ids.ButtonLeftPagination.disabled = False

                #global_rv.ButtonLeftPagination.disabled = True if global_rv.StartPagination <= 0 else False 
            #Flecha de la derecha
            case "right":

                #Activa el boton de la izquierda de la paginacion
                global_rv[rv].objecto.ids.ButtonLeftPagination.disabled = False

                #IF Statement, si la cantidad de items de la paginación es mayor a los items del diccionario
                #el DISABLED sera True, en caso contrario será False
                if global_rv[rv].objecto.ItemsAccountPagination >= len(global_rv[rv].objecto.DictionaryDataset):

                    #Desactiva boton derecho
                    global_rv[rv].objecto.ids.ButtonRightPagination.disabled = True

                else: 
                    #Activa boton derecho
                    global_rv[rv].objecto.ids.ButtonRightPagination.disabled = False

            #Ambas flechas
            case "both":

                #left

                #IF Statement, si el inicio de la paginación es 0 DISABLED es True desactivando el boton izquierdo 
                #caso contrario DISABLED es False activando el boton 
                if RecycleViewTable.StartPagination <= 0:
                    #Desactiva boton izquierdo
                    global_rv[rv].objecto.ids.ButtonLeftPagination.disabled = True 

                else:
                    #Activa boton izquierdo
                    global_rv[rv].objecto.ids.ButtonLeftPagination.disabled = False

                #right

                #IF Statement, si la cantidad de items de la paginación es mayor a los items del diccionario
                #el DISABLED sera True, en caso contrario será False
                if global_rv[rv].objecto.ItemsAccountPagination >= len(global_rv[rv].objecto.DictionaryDataset):

                    #Desactiva boton derecho
                    global_rv[rv].objecto.ids.ButtonRightPagination.disabled = True

                else: 
                    #Activa boton derecho
                    global_rv[rv].objecto.ids.ButtonRightPagination.disabled = False
            case _:
                pass


############
