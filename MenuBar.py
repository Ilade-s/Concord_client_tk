from tkinter import *
#from tkinter import filedialog as fldialog  # Choix de fichier etc...
# Messages d'information ou d'avertissement
from tkinter import messagebox as msgbox
from EventFrame import EventFrame

class MenuBar(Menu):
    """
    Menu qui s'affiche à gauche dans l'application tkinter

    Affiche les actions possibles en fonction de MainFrame
    """

    def __init__(self, master) -> None:
        super().__init__(master)
        self.eventFrame = None
        self.master = master
        # Création des menus déroulants    
        self.create_connect_menu()
        # ajout about
        self.add_command(
            label="About", command=lambda: msgbox.showinfo("About",
                    f"Concord client v{self.master.version}\nMade by {self.master.authors}, 2021 \
                    \nSource : https://github.com/Ilade-s/Concord_client_tk \
                    \nAssets : https://feathericons.com/"))

    def create_connect_menu(self):
        connectMenu = Menu(self, tearoff=False)
        self.add_cascade(label="Connect", underline=0, menu=connectMenu)

        connectMenu.add_command(
            label="Create room as host...", command=self.create_room)
        connectMenu.add_command(
            label="Join room as guest...", command=self.join_room)
    
    def create_room(self):
        if self.eventFrame: self.eventFrame.destroy()
        self.eventFrame = EventFrame(self.master.contentFrame, 'connexion', True)

    def join_room(self):
        if self.eventFrame: self.eventFrame.destroy()
        self.eventFrame = EventFrame(self.master.contentFrame, 'connexion', False)

        