from kivy.metrics import dp


from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch

import weakref

class ChargeAddPage(MDScreen):

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active', 'and', value, ' value')
        else:
            print('The checkbox', checkbox, 'is inactive')

    def DeleteItemCharge(self):

        #Elimina el último item nuevo producto
        self.ids.BoxLayoutChargeAdd.remove_widget(self.ids.BoxLayoutChargeAdd.children[0])

        try:
            #Creacion de widget de eliminar producto
            NewButton = MDFloatingActionButton(

                    icon= "account-plus",
                    type= "small",
                    #on_release= self.AddItemCharge(),
                    on_release= lambda x='Item configuracion': self.AddItemCharge('NewGridName', 'NewButtonAddItem'),
                    elevation= 0,
                    pos_hint= {'center_x': .5, 'center_y': .5}
                )

            # Remueve el Button de añadir producto
            self.ids.BoxLayoutChargeAdd.children[0].remove_widget(self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem)

            #Añade el nuevo Button para eliminar producto
            self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButton)
            
            #Le agrega un id al nuevo Button
            self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton)

            if len(self.ids.BoxLayoutChargeAdd.children) >= 2:
                NewButton = MDFloatingActionButton(

                        icon= "delete",
                        type= "small",
                        #on_release= self.AddItemCharge(),
                        on_release= lambda x='': self.DeleteItemCharge(),
                        elevation= 0,
                        pos_hint= {'center_x': .5, 'center_y': .5}
                    )

                #Actualiza numero de columnas
                self.ids.BoxLayoutChargeAdd.children[1].cols = 5
                #Lo añade al Padre
                self.ids.BoxLayoutChargeAdd.children[1].add_widget(NewButton)
                #Se le da un identificador al widget boton de eliminar
                self.ids.BoxLayoutChargeAdd.children[1].ids.NewButtonAddItem = weakref.ref(NewButton)
                print('hay mas')
            else:

                '''
                if len(self.ids.BoxLayoutChargeAdd.children) == 1:


                    #Creacion del widget boton para eliminar producto
                    NewButtonDelete = MDFloatingActionButton(

                            icon= "delete",
                            type= "small",
                            #on_release= self.AddItemCharge(),
                            on_release= lambda x='': self.DeleteItemCharge(),
                            elevation= 0,
                            pos_hint= {'center_x': .5, 'center_y': .5}
                        )


                    #Lo añade al Padre
                    self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButtonDelete)
                    #Se le da un identificador al widget boton de eliminar
                    self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButtonDelete)
                '''
                print('NOOO hay mas')
        except AttributeError:

            #Creacion de widget de eliminar producto
            NewButton = MDFloatingActionButton(

                    icon= "account-plus",
                    type= "small",
                    #on_release= self.AddItemCharge(),
                    on_release= lambda x='Item configuracion': self.AddItemCharge('NewGridName', 'NewButtonAddItem'),
                    elevation= 0,
                    pos_hint= {'center_x': .5, 'center_y': .5}
                )

            
            #Actualiza numero de columnas
            self.ids.BoxLayoutChargeAdd.children[0].cols = 5

            #Añade el nuevo Button para eliminar producto
            self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButton)
            
            #Le agrega un id al nuevo Button
            self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton)
            pass

            

    def AddItemCharge(self, ParentWidget, ChildrenWidget):


        #remueve el boton de añadir
        try:
            self.ids[ParentWidget].remove_widget(self.ids[ChildrenWidget])
            #self.ids[ParentWidget].cols = 5

            NewButtonDelete = MDFloatingActionButton(

                        icon= "delete",
                        type= "small",
                        #on_release= self.AddItemCharge(),
                        on_release= lambda x='': self.DeleteItemCharge(),
                        elevation= 0,
                        pos_hint= {'center_x': .5, 'center_y': .5}
                    )
            
        
            #Lo añade al Padre
            self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButtonDelete)
            #Se le da un identificador al widget boton de eliminar
            self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButtonDelete)
            print('try')
    
        #Permite que se elimine usando los "weakref"
        except KeyError:

            print('keyerror')

            
            if len(self.ids.BoxLayoutChargeAdd.children) == 1:

                self.ids.BoxLayoutChargeAdd.children[0].remove_widget(self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem)
            

                #Creacion del widget boton para eliminar producto
                NewButton2 = MDFloatingActionButton(

                        icon= "delete",
                        type= "small",
                        #on_release= self.AddItemCharge(),
                        on_release= lambda x='': self.DeleteItemCharge(),
                        elevation= 0,
                        pos_hint= {'center_x': .5, 'center_y': .5}
                    )


                #Lo añade al Padre
                self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButton2)
                #Se le da un identificador al widget boton de eliminar
                self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton2)

            #self.ids.BoxLayoutChargeAdd.children[0].cols = 5
            
            #Si la cantidad de items es mayor a 2, entonces me eliminas del antepenultimo item el boton de eliminar o agregar
            if len(self.ids.BoxLayoutChargeAdd.children) >= 2:
                print('if')
                self.ids.BoxLayoutChargeAdd.children[1].cols = 4
                self.ids.BoxLayoutChargeAdd.children[1].remove_widget(self.ids.BoxLayoutChargeAdd.children[1].ids.NewButtonAddItem)


                #Remueve el boton de añadir del último item
                self.ids.BoxLayoutChargeAdd.children[0].remove_widget(self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem)

                #Creacion del widget boton para eliminar producto
                NewButton2 = MDFloatingActionButton(

                        icon= "delete",
                        type= "small",
                        #on_release= self.AddItemCharge(),
                        on_release= lambda x='': self.DeleteItemCharge(),
                        elevation= 0,
                        pos_hint= {'center_x': .5, 'center_y': .5}
                    )


                #Lo añade al Padre
                self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButton2)
                #Se le da un identificador al widget boton de eliminar
                self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton2)

                


        #Crea lista de los nombre de los MDLabel que se crearan
        itemListLabel = ['Producto', 'Cantidad', 'Precio']

        #Crea el MDGridLayout donde se guardará todo
        NewGridLayout = MDGridLayout(
                cols= 5,
                spacing= dp(20),
                padding= [dp(1), dp(5), dp(1), dp(1)],
                
                size_hint_y= None,
                height= dp(60)
            )

        #For loop que creará los MDlabel segun el array itemListLabel
        for item in itemListLabel:
            
            #crea el widget
            NewLabels = MDTextField(
                        mode= 'rectangle',
                        text= '',
                        hint_text= item,
                    )
            
            #Lo añade al grid creado desde el comienzo
            NewGridLayout.add_widget(NewLabels)


        #Crea un MDGridLayout hijo del creado al comienzo
        ChildreNewGridLayout = MDGridLayout(
            cols=1,
            adaptive_height= True,
            size_hint_x= None,
            width= self.ids.SwitchChargeAdd.width * 2

        )

        #Se crea el MDSwitch 
        NewLabelSwitch = MDSwitch(
                    
                pos_hint= {'center_x': 0.05, 'center_y': -0.5},
                icon_active= "check",

                #on_active= self.on_checkbox_active(*args)
            )

        #Se añade al MDgridLayout hijo
        ChildreNewGridLayout.add_widget(NewLabelSwitch)

        #Se añade el MDGridLayout hijo al padre
        NewGridLayout.add_widget(ChildreNewGridLayout)

        ############################

        #NOMBRE DEL NUEVO GRID Y BUTTON
        NewGridName = 'NewGrid' + str(len(self.ids.BoxLayoutChargeAdd.children))
        #NewButtonName = 'NewButtonAddItem' #+ str(len(self.ids.BoxLayoutChargeAdd.children))

        #Se crea boton para poder añadir otro item
        NewButton = MDFloatingActionButton(

                    icon= "account-plus",
                    type= "small",
                    #on_release= self.AddItemCharge(),
                    on_release= lambda x='Item configuracion': self.AddItemCharge('NewGridName', 'NewButtonAddItem'),
                    elevation= 0,
                    pos_hint= {'center_x': .5, 'center_y': .5}
                )

        #Se añade el nuevo boton al MDGridLayout Padre
        NewGridLayout.add_widget(NewButton)
        

        #Se añade el widget MDGridLayout al MDBoxLayout existente en kivy
        self.ids.BoxLayoutChargeAdd.add_widget(NewGridLayout)

        #Se le añade un ID al nuevo MDGridLayout
        self.ids.BoxLayoutChargeAdd.ids[NewGridName] = weakref.ref(NewGridLayout)
        #Se le añade el ID al nuevo boton 'añadir producto'
        self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButton)

        '''
        if len(self.ids.BoxLayoutChargeAdd.children) <= 2:

            self.ids.BoxLayoutChargeAdd.children[0].cols = 7

            #Creacion del widget boton para eliminar producto
            NewButtonDelete = MDFloatingActionButton(

                    icon= "delete",
                    type= "small",
                    #on_release= self.AddItemCharge(),
                    on_release= lambda x='': self.DeleteItemCharge(),
                    elevation= 0,
                    pos_hint= {'center_x': .5, 'center_y': .5}
                )


            #Lo añade al Padre
            self.ids.BoxLayoutChargeAdd.children[0].add_widget(NewButtonDelete)
            #Se le da un identificador al widget boton de eliminar
            self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem = weakref.ref(NewButtonDelete)

            pass
        '''

        '''
        print()
        print(str(self) + ' <--- SELF')
        print(str(self.ids.BoxLayoutChargeAdd.ids[NewGridName]) + ' <--- IDS BOXLAYOUTCHARGEADD-NewGridName')
        print(str(self.ids.BoxLayoutChargeAdd.children[0].ids.NewButtonAddItem) + ' <--- CHILDREN[0].ids')
        print(str(self.ids[ParentWidget]) + ' <--- PARENT WIDGET')
        print()
        '''
    