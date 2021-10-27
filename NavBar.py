"""
Sous fichier de client.py : 
Contient la frame située en bas de la fenêtre 
TODO
"""
from tkinter import *
from tkinter import ttk, filedialog as fldial, messagebox as msgbox
from datetime import datetime
import os
from imgHandler import *

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
        self.connexionStatusLabel['text'] = f'Connexion : {ip} ' + ('(host)' if ashost else '(client)')
    
    def reset(self):
        for c in self.winfo_children():
            c.destroy()
        self.__create_widgets()

class InputFrame(Frame):

    def __init__(self, master) -> None:
        super().__init__(master, background=master['background'],
                        relief=RAISED)
        self.place(relx=.25, rely=0, relheight=1, relwidth=.75)
        self.__create_widgets()
    
    def __create_widgets(self):
        def send_msg(event=None):
            if not msg.get() or not self.master.master.log: return 0 # exits if msg is empty or if client is not connected
            msgDict = {
                'pseudo': self.master.master.pseudo,
                'time': datetime.now().strftime('%H:%M'), # current time (format HH:MM)
                'content': msg.get(),
                'distant': False,
                'info': False
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
        
        def send_image():
            path = fldial.askopenfilename(initialdir=os.getcwd(), title="Image to compress...")
            name = path.split('/')[-1].split('.')[0]
            msgDict = {
                'pseudo': self.master.master.pseudo,
                'time': datetime.now().strftime('%H:%M'), # current time (format HH:MM)
                'content': name,
                'distant': False,
                'info': False,
                'img': path
            }
            self.master.master.contentFrame.set_new_msg(msgDict)
            try:
                csv_folder_path = 'img/' + name + '/'              
                if not os.path.exists(csv_folder_path): os.makedirs(csv_folder_path)
                (csv_path, motifs_path) = convert_image(path, 32, csv_folder_path)
                len_img = get_len_img(path)
                # send info message
                self.master.master.network.SendMessage(f'IMG%INFO%{name}%{len_img}')
                # sends each line of the image
                for line, i in zip(get_lines(csv_path), range(len_img)):
                    print(f'sending line {i+1} out of {len_img}')
                    line_str = ','.join(line)
                    #print(f'IMG%LINE%{name}%{line_str}')
                    self.master.master.network.SendMessage(f'IMG%LINE%{name}%{line_str}')
                # sends each line of the motifs
                for line, i in zip(get_motifs(motifs_path), range(len_img)):
                    print(f'sending motif {i+1}')
                    line_str = ','.join(line)
                    self.master.master.network.SendMessage(f'IMG%MOTIF%{name}%{line_str}')
                # send end message to confirm end of data sending
                self.master.master.network.SendMessage(f'IMG%END%{name}')
            except Exception as e:
                print(f'An execption occurred when sending the image at path {path} : {e}') 
                msgbox.showerror('Send image', f'invalid image, please try again with another one : {e}')
        
        msg = StringVar()
        msg.set('new message...')

        self.imgIcon = PhotoImage(file="assets/img_icon.png")
        ttk.Button(self, text='envoyer une image', image=self.imgIcon, command=send_image
            ).place(relx=.025, rely=.1)

        MsgLabel = Entry(self, textvariable=msg, background='#A8B8FF', font=("Arial", 15))
        MsgLabel.place(relx=.175, rely=.1, relwidth=.9, relheight=.8, anchor='nw')
        # Entry bindings
        MsgLabel.bind('<1>', entry_clicked)
        MsgLabel.bind('<Return>', send_msg)