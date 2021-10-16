"""
Sous fichier de client.py : 
Contient la frame située en bas de la fenêtre 
TODO
"""
from tkinter import *
from tkinter import ttk

class NavBar(LabelFrame):

    def __init__(self, master) -> None:
        super().__init__(master, background="#A8B8FF",
                         relief=RAISED)
        self.place(relx=0, rely=.8, relheight=.2, relwidth=1)

    def setup_subframes(self):
        self.messageFrame = MessageFrame(self)
        self.inputFrame = InputFrame(self)

class MessageFrame(Frame):

    def __init__(self, master) -> None:
        super().__init__(master, background=master['background'],
                        relief=RAISED)
        self.place(relx=.2, rely=0, relheight=1, relwidth=.8)

class InputFrame(LabelFrame):

    def __init__(self, master) -> None:
        super().__init__(master, background=master['background'], text="Navigation",
                        relief=RAISED)
        self.place(relx=0, rely=1, relheight=1, relwidth=.2)