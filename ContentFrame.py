"""
Sous fichier de client.py :
Contient la frame, qui séra séparée en un cadre pour afficher les message et un cadre en bas pour écrire
TODO
"""
from tkinter import *
from tkinter import ttk
from EventFrame import *

class ContentFrame(Frame):

    def __init__(self, master) -> None:
        super().__init__(master, background="#993441",
                        relief=RAISED)
        self.place(relx=.25, rely=0, relheight=1, relwidth=.75)
        self.setup_subframes()
    
    def setup_subframes(self):
        self.messageFrame = MessageFrame(self)
        self.inputFrame = InputFrame(self)
        #self.eventFrame = EventFrame(self)

class MessageFrame(Frame):

    def __init__(self, master) -> None:
        super().__init__(master, background=master['background'],
                        relief=RAISED)
        self.place(relx=0, rely=0, relheight=.8, relwidth=1)

class InputFrame(Frame):

    def __init__(self, master) -> None:
        super().__init__(master, background="#FFB8CD",
                        relief=RAISED)
        self.place(relx=0, rely=.8, relheight=.2, relwidth=1)