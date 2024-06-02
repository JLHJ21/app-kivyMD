from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager

from kivy.core.window import Window
import os

#Clase para la seleccion de fotos, pagina
class ChargeChooseImagePage(MDScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        Window.bind(on_keyboard=self.events)
        #self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, 
            select_path=self.select_path,
            preview=True,
            icon_selection_button="pencil",
        )
    
    #Abre el seleccionador
    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        #self.manager_open = True

    #Archivo seleccionado
    def select_path(self, path: str):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''

        #Cambia el source de la imagen
        #self.manager.get_screen("StorePageUpdate").ids.imageProduct.source = path

        #Cambia la pagina
        self.manager.current = 'ChargeAddPage'

        self.exit_manager()
        #toast(path)

    #Permite cerrar el seleccionador
    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        #self.manager_open = False
        self.manager.current = 'ChargeAddPage'
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True
    
    def changeTextImage(self):
        #self.manager.get_screen("StorePageUpdate").ids.imageProduct.source = path
        pass