"""
Sous fichier de client.py :
Contient la frame, qui séra séparée en un cadre pour afficher les message et un cadre en bas pour écrire
TODO
"""
from tkinter import *
from tkinter import ttk
from EventFrame import *

defaultMessage = {
    'pseudo': 'Pedro',
    'time': '17:50',
    'content': 'elo, me llamo Pedro',
    'distant': True
}
defaultMessage2 = {
    'pseudo': 'You',
    'time': '17:51',
    'content': 'elo',
    'distant': False
}

class ContentFrame(Frame):

    def __init__(self, master) -> None:
        super().__init__(master, background="#292D3E",
                        relief=RAISED)
        self.place(relx=0, rely=0, relheight=.8, relwidth=1)
        #self.eventFrame = EventFrame(self)
        mess1 = MessageTemplate(self)
        mess2 = MessageTemplate(self, defaultMessage2)

class MessageTemplate(LabelFrame):

    def __init__(self, master, message=defaultMessage, fontSize=12) -> None:
        """
        Crée et packe un message dans master (ContentFrame)
        message : dictionnaire qui contient toutes les informations sur le message
        """
        super().__init__(master, background=master['background'], 
                        text=f"{message['pseudo']} ({message['time']})",
                        relief=RAISED, foreground='white')
        # ajout texte
        ttk.Label(self, text=message['content'], style="Message.TLabel"
            , background='#292D3E', foreground='white').pack(padx=5, pady=2)
        # configure style
        s = ttk.Style(self)
        s.configure("Message.TLabel", font=("Arial", fontSize))

        self.pack(anchor="nw" if message['distant'] else "ne", padx=5)
        
    