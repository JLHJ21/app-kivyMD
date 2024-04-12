from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen

#Acomoda la resolución de la ventada, OJO solo para uso de desarrollo
#from kivy.core.window import Window
#Window.size = (720 , 1600)

Builder.load_string('''
                    
<LabelTable@MDLabel>:
    halign: "center"
    markup: True

<SelectableLabel>:
    # Draw a background to indicate selection
                    
    canvas.before:
        Color:
            rgba: (.0, 0.9, .7, 1) if self.selected else (0, 0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size
        Line:
            points: (*self.pos, self.right, self.y)
                    
    pos: self.pos
    size: self.size
                    
    Image:
        id: id_imagen
        
        source: "logo.jpg"       
                                 
        allow_stretch: True
        keep_ratio: False 
                    
        fit_mode: "scale-down"
        size_hint: 1, 1

        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Rectangle:
                pos: self.pos
                size: self.size


    LabelTable:
        id: id_nombre
        text: "Nombre"

    LabelTable:
        id: id_proveedor
        text: "Proveedor"
                    
    LabelTable:
        id: id_cantidad
        text: "Cantidad"
                    
    LabelTable:
        id: id_precio
        text: "Precio"


<RV>:
                    
    rv: rv # expose the widget
       
    MDBoxLayout:
        orientation: 'vertical'

        MDGridLayout:
            adaptive_height: True
            cols: 1
                    
            MDGridLayout:    
                            
                cols: 5
                                        
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: dp(56)
                    
                canvas.before:
                    Color:
                        rgba: (0, 0, 255, .6)
                    Rectangle:
                        pos: self.pos
                        size: self.size
                                       
                LabelTable:
                    text: "Imagen"
                    font_style: "H6"

                LabelTable:
                    text: "Nombre"
                    font_style: "H6"

                LabelTable:
                    text: "Proveedor"
                    font_style: "H6"
                                
                LabelTable:
                    text: "Cantidad"
                    font_style: "H6"
                                
                LabelTable:
                    text: "Precio"
                    font_style: "H6"
                
        RecycleView:  
                    
            id: rv

            viewclass: 'SelectableLabel'
                            
            SelectableRecycleBoxLayout:
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                multiselect: True
                touch_multiselect: True
                    
        MDGridLayout:
            cols:3
            padding: dp(36), dp(8)
            adaptive_height: True
                    
            canvas.before:
                Color:
                    rgba: (0, 0, 255, .6)
                Rectangle:
                    pos: self.pos
                    size: self.size
                    
            MDBoxLayout:
                size_hint_x: .35
            
                MDLabel:
                    id: ItemsShowed
                    text: "Mostrando: 1-5 de 10"
                    halign: "left"
                    font_style: "Subtitle1"
            


            AnchorLayout:
                size_hint_x: .55
                size_hint_y: None
                height: ButtonLeftPagination.height
            
            
                anchor_x:'center'
                anchor_y:'bottom'
                                                
                MDRectangleFlatIconButton:
                    id: ItemsAmount
                    icon: "android"
                    text: ""
                    font_style: "Subtitle1"
                    
                    md_bg_color: "white"
                    
                    text_color: "black"

                    line_color: "orange"
                    icon_color: "orange"

                    on_release:
                        root.ChangeItemsAmount()
                        
            
            AnchorLayout:
                size_hint_y: None
                height: ButtonLeftPagination.height
                size_hint_x: .3
            
                anchor_x:'right'
                anchor_y:'bottom'
            
                MDBoxLayout:
                    orientation: "horizontal"
                    size_hint: None, None
                    size: self.minimum_size
                    spacing: dp(10)
            
                    MDFloatingActionButton:
                        id: ButtonLeftPagination
            
                        icon: "arrow-left-bold-outline"
                        type: "small"
                        theme_icon_color: "Custom"
                        md_bg_color: "#fefbff"
                        text_color: "#6851a5"
                        elevation: 0
                        disabled: True
                    
                        on_release:
                            root.ChangeItemsAmountButtons("left")
                
                    MDFloatingActionButton:
                        id: ButtonRightPagination
                        icon: "arrow-right-bold-outline"
                        type: "small"
                        theme_icon_color: "Custom"
                        md_bg_color: "#fefbff"
                        text_color: "#6851a5"
                        elevation: 0
                        disabled: False
                    
                        on_release:
                            root.ChangeItemsAmountButtons("right")

                    
''')

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, MDGridLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
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
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class RV(MDScreen):

    #Cantidad de items que se mostrará en el RecycleView
    StartPagination = 0
    ItemsAccountPagination = 5

    #Variable estaticas que permiten, el uso de los botones para la paginación
    StaticStartPagination = StartPagination
    StaticItemsAccountPagination = ItemsAccountPagination

    #Diccionario donde se almacenaran los datos
    DictionaryDataset = {}

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

        #Texto de la cantidad de items que se muestran
        self.ids.ItemsAmount.text = "Items por página: " + str(self.ItemsAccountPagination)

        #dictionary donde estará todos los datos de la tabla
        for i in range(1,21):

            d = {f"dato{i}": [f"dato{i}_nombre", f"dato{i}_proveedor", f"dato{i}_cantidad", f"dato{i}_precio",]}
            self.DictionaryDataset.update(d)
        
        #Llama la función TableData para rellenar los datos de la tabla
        self.TableData(self.DictionaryDataset)

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

                    }
                #Agregar a la tabla los items
                self.rv.data.append(d)

                #Suma el valor a la paginacion
                IterationStartPagination += 1  
            else:
                #Si el comienzo y el final de la paginacion son iguales o mayores, se rompe el ciclo FOR
                break

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

        #Llama la función TableData para rellenar los datos de la tabla
        self.TableData(self.DictionaryDataset)

        #Cambia el texto del boton ItemsAmount
        self.ids.ItemsAmount.text = "Items por página: " + str(self.ItemsAccountPagination)

        self.StatusButtonPagination("both")

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

class TestApp(MDApp):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()