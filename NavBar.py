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
        self.master = master
        self.__setup_subframes()
        self.place(relx=0, rely=.8, relheight=.2, relwidth=1)

    def __setup_subframes(self):
        self.infoFrame = InfoFrame(self)
        self.inputFrame = InputFrame(self)

class InfoFrame(LabelFrame):

    def __init__(self, master) -> None:
        super().__init__(master, background='#7985DF', text='Statut client',
                        relief=RAISED, foreground='white')
        self.master = master
        self.place(relx=0, rely=0, relheight=1, relwidth=.25)
        self.__create_widgets()
    
    def __create_widgets(self):
        self.connexionStatusLabel = ttk.Label(self, text='Connexion : aucune',
            background=self['background'], style='Info.TLabel')

        self.connexionStatusLabel.pack(padx=2, pady=3)

        self.renderedMsgsLabel = ttk.Label(self, 
                text='Messages affichés : /',
                background=self['background'], style='Info.TLabel'
                )
        
        self.renderedMsgsLabel.pack(padx=2, pady=3)

        self.LogLabel = ttk.Label(self, text='Log file : ...',
            background=self['background'], style='Info.TLabel')
        
        self.LogLabel.pack(padx=2, pady=3)

        s = ttk.Style(self)
        s.configure("Info.TLabel", font=("Arial", 12))
    
    def update_renderLabel(self, newindex, n_rnd_msgs):
        self.renderedMsgsLabel['text'] = 'Messages affichés : {} to {}'.format(
                newindex, newindex + n_rnd_msgs)
    

class InputFrame(Frame):

    def __init__(self, master) -> None:
        super().__init__(master, background=master['background'],
                        relief=RAISED)
        self.place(relx=.25, rely=0, relheight=1, relwidth=.75)