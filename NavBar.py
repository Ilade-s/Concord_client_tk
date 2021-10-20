"""
Sous fichier de client.py : 
Contient la frame située en bas de la fenêtre 
TODO
"""
from tkinter import *
from tkinter import ttk
from datetime import datetime

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
                background=self['background'], style='Info.TLabel')
        
        self.renderedMsgsLabel.pack(padx=2, pady=3)

        self.LogLabel = ttk.Label(self, text='Log file : ...',
            background=self['background'], style='Info.TLabel')
        
        self.LogLabel.pack(padx=2, pady=3)

        s = ttk.Style(self)
        s.configure("Info.TLabel", font=("Arial", 12))
    
    def update_renderLabel(self, newindex, n_rnd_msgs):
        self.renderedMsgsLabel['text'] = 'Messages affichés : {} to {}'.format(
                newindex, newindex + n_rnd_msgs)
    
    def update_logLabel(self, filename):
        self.LogLabel['text'] = 'log : ' + filename
    
    def update_connexionLabel(self, ip, ashost):
        """
        ip : str
        ashost : bool
        """
        self.connexionStatusLabel['text'] = f'Connexion : {ip} ' + '(host)' if ashost else '(client)'
    

class InputFrame(Frame):

    def __init__(self, master) -> None:
        super().__init__(master, background=master['background'],
                        relief=RAISED)
        self.place(relx=.25, rely=0, relheight=1, relwidth=.75)
        self.__create_widgets()
    
    def __create_widgets(self):
        def send_msg(event=None):
            if not msg.get(): return 0 # exits if msg is empty
            msgDict = {
                'pseudo': self.master.master.pseudo,
                'time': datetime.now().strftime('%H:%M'), # current time (format HH:MM)
                'content': msg.get(),
                'distant': False
            }
            self.master.master.log.add_message(msgDict)
            self.master.master.contentFrame.set_new_msg(msgDict)
            self.master.master.network.SendMessage(msgDict['content'])
            # reset entry
            msg.set('')
            if not event:
                MsgLabel['background'] = self['background']
                msg.set('new message...')
        
        def entry_clicked(event):
            if msg.get() == 'new message...':
                msg.set('')
            event.widget['background'] = '#424864'
            event.widget.focus_set()
        
        msg = StringVar()
        msg.set('new message...')

        MsgLabel = Entry(self, textvariable=msg, background='#A8B8FF', font=("Arial", 15))
        MsgLabel.place(relx=.05, rely=.1, relwidth=.9, relheight=.8, anchor='nw')
        # Entry bindings
        MsgLabel.bind('<1>', entry_clicked)
        MsgLabel.bind('<Return>', send_msg)