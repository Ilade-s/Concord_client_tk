from tkinter import *
#from tkinter import filedialog as fldialog  # Choix de fichier etc...
# Messages d'information ou d'avertissement
from tkinter import messagebox as msgbox

class MenuBar(Menu):
    """
    Menu qui s'affiche à gauche dans l'application tkinter

    Affiche les actions possibles en fonction de MainFrame
    """

    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        # Création des menus déroulants
        # TODO
        # ajout about
        self.add_command(
            label="About", command=lambda: msgbox.showinfo("About",
                    f"Concord client v{self.master.version}\nMade by {self.master.authors}, 2021 \
                    \nSource : https://github.com/Ilade-s/Concord_client_tk \
                    \nAssets : https://feathericons.com/"))