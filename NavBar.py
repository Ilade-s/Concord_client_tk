"""
Sous fichier de client.py : 
Contient la frame panneau située à gauche, où on fait ses choix (boutons) et configure la connexion
TODO
"""
from tkinter import *
from tkinter import ttk

class NavBar(LabelFrame):

    def __init__(self, master) -> None:
        super().__init__(master, background="#A8B8FF",
                         relief=RAISED, text="Menu de navigation")
        self.place(relx=0, rely=0, relheight=1, relwidth=.25)