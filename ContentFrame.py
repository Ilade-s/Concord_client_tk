"""
Sous fichier de client.py :
Contient la frame, qui séra séparée en un cadre pour afficher les message et un cadre en bas pour écrire
TODO
"""
from tkinter import *
from tkinter import ttk
from EventFrame import *
import time
from threading import Thread #Permet de faire tourner des fonctions en meme temps (async)
from imgHandler import ImgReceiving, make_img_path, os

defaultMessage = {
    'pseudo': 'Pedro',
    'time': '17:50',
    'content': 'elo, me llamo Pedro',
    'distant': True
}
defaultMessage2 = {
    'pseudo': 'Anon',
    'time': '17:51',
    'content': 'eloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo',
    'distant': False
}

class ContentFrame(Frame):

    def __init__(self, master) -> None:
        super().__init__(master, background="#292D3E",
                        relief=RAISED)
        self.place(relx=0, rely=0, relheight=.8, relwidth=1)
        #self.eventFrame = EventFrame(self)
        self.msgList = []
        self.allmsgList = []
        self.rendered_msgs = []
        self.member_list = []
        self.img_to_receive = {}
        self.msgIndex = 0
        #self.__debug_setup()
        self.msgStart = False
    
    def __debug_setup(self):
        for _ in range(10):
            self.msgList.append(defaultMessage)
            self.msgList.append(defaultMessage2)
    
    def setup_join(self):
        self.msgStart = True
        GetMessage = Thread(target=self.update_message_server)
        GetMessage.start()
    
    def stop_update(self):
        self.msgStart = False
    
    def reset_frame(self):
        self.msgList = []
        self.render_msgs()
    
    def show_last_msg(self):
        """
        render_msgs which go to the last messages
        """
        nMsgs_renderable = self.get_maxAff()
        self.msgIndex = len(self.msgList) - nMsgs_renderable
        if self.msgIndex < 0: self.msgIndex = 0
        self.render_msgs()
    
    def scroll_msgs(self, event):
        if (event.num == 5 or event.delta == -120) and self.msgIndex < len(self.msgList) - 1:
            self.msgIndex += 1
        if (event.num == 4 or event.delta == 120) and self.msgIndex > 0:
            self.msgIndex -= 1
        self.render_msgs()
    
    def set_new_msg(self, newmsg):
        """
        sends new message and renders it automatically
        """
        self.msgList.append(newmsg)
        self.show_last_msg()
    
    def render_msgs(self):
        def format_content(txt, maxCarac):
            if len(txt) > maxCarac:
                return format_content(txt[:maxCarac//2], maxCarac) + '\n' + \
                        format_content(txt[maxCarac//2:], maxCarac)
            else: 
                return txt

        for msg in self.rendered_msgs:
            msg.destroy()
        self.rendered_msgs = []
        
        nMsgs_renderable = self.get_maxAff()
        msgs_to_render = self.msgList[self.msgIndex:self.msgIndex + nMsgs_renderable]

        for msg in msgs_to_render:
            if 'img' not in msg.keys(): # text message
                msgc = msg.copy()
                msgc['content'] = format_content(msgc['content'], self.get_maxCarac())
                self.rendered_msgs.append(MessageTemplate(self, msgc))
            else: # image message
                img_path = msg['img'] if os.path.exists(msg['img']) else make_img_path(msg['img'])
                self.rendered_msgs.append(ImageTemplate(self, msg, img_path))

        
        self.master.navBar.infoFrame.update_renderLabel(self.msgIndex + 1, len(msgs_to_render) - 1)

    def get_maxAff(self):
        currentY = self.winfo_height()
        if currentY != 1:    
            maxMsgs = currentY // 50
        else:    
            maxMsgs = 8
        return maxMsgs
    
    def get_maxCarac(self):
        currentX = self.winfo_width()
        if currentX != 1:    
            maxMsgs = currentX // 10
        else:    
            maxMsgs = 100
        return maxMsgs

    def update_message_server(self):
        while self.msgStart:
            time.sleep(1)
            new_msgs = False
            new_img = False
            msg = self.master.network.FetchMessage()
            for cle, element in msg.copy().items():
                if cle > len([msg for msg in self.allmsgList if msg['distant']]):
                    if element['error']:
                        if element['error'] == 'DISCONNECTED':
                            msgbox.showerror('Déconnexion', "Vous avez été déconnecté.\tLe client va redémarrer...")
                            self.stop_update()
                            self.master.log = None
                            self.master.network.CloseClient(False)
                            self.reset_frame()
                            self.master.navBar.infoFrame.reset()
                            self.master.Menu.show_connect_menu()
                            return 0
                    elif element['distant']:
                        if 'IMG%' in element['content']: # img msg (info or part)
                            print(element['content'])
                            msg_type = element['content'].split('%')[1]
                            if msg_type == 'INFO': # image infos
                                name = element['content'].split('%')[2]
                                len_img = element['content'].split('%')[3]
                                self.img_to_receive[name] = ImgReceiving(name, len_img)
                            elif msg_type == 'END':
                                name = element['content'].split('%')[2]
                                self.img_to_receive[name].save_motifs()
                                self.img_to_receive[name].save_conversion()
                                element['content'] = name
                                element['img'] = name
                                # convert then show the image
                                self.img_to_receive[name].retrieve_img_from_CSV()
                                self.msgList.append(element)
                                new_img = True
                            elif msg_type == 'LINE': # part of an image
                                (name, line) = element['content'].split('%')[2:]
                                self.img_to_receive[name].add_line(line)
                            elif msg_type == 'MOTIF': # part of an image
                                (name, line) = element['content'].split('%')[2:]
                                self.img_to_receive[name].add_motif(line)
                        else:
                            self.msgList.append(element)
                            self.master.log.add_message(element)
                            new_msgs = True
                            if element['pseudo'] not in self.member_list and element['pseudo'] != 'INFO!':
                                self.member_list.append(element['pseudo'])
                                self.master.log.add_member(element['pseudo'])
                        self.allmsgList.append(element)

            if (new_msgs and len(self.msgList) - self.msgIndex < self.get_maxAff()) or new_img:
                self.render_msgs()

class MessageTemplate(LabelFrame):

    def __init__(self, master, message=defaultMessage, fontSize=12) -> None:
        """
        Crée et packe un message dans master (ContentFrame)
        message : dictionnaire qui contient toutes les informations sur le message
        """
        super().__init__(master, background=master['background'], 
                        text=f"{message['pseudo']} ({message['time']})" if message['distant'] 
                            else f"{message['pseudo']} (You) ({message['time']})",
                        relief=RAISED, foreground='white')
        # ajout texte
        msgLabel = ttk.Label(self, text=message['content'], style="Message.TLabel"
            , background='#292D3E', foreground='white')
        msgLabel.pack(padx=5, pady=2)
        # configure style
        s = ttk.Style(self)
        s.configure("Message.TLabel", font=("Arial", fontSize))
        # find good anchor
        if message['info']:
            anchor = CENTER
            msgLabel['background'] = 'white'
            msgLabel['foreground'] = 'black'
            self['background'] = 'white'
            self['foreground'] = 'black'
            self['text'] = 'INFORMATION'
        elif message['distant']:
            anchor = "nw"
        else:
            anchor = "ne"
        self.pack(anchor=anchor, padx=5)

class ImageTemplate(LabelFrame):

    def __init__(self, master, message, image_path, fontSize=12) -> None:
        """
        Crée et packe un message dans master (ContentFrame)
        message : dictionnaire qui contient toutes les informations sur le message
        """
        super().__init__(master, background=master['background'], 
                        text=f"{message['pseudo']} ({message['time']})" if message['distant'] 
                            else f"{message['pseudo']} (You) ({message['time']})",
                        relief=RAISED, foreground='white')
        # ajout texte
        self.img = PhotoImage(file=image_path)
        msgLabel = ttk.Label(self, text=message['content'], style="Message.TLabel"
            ,image=self.img , background='#292D3E', foreground='white')
        msgLabel.pack(padx=5, pady=2)
        # configure style
        s = ttk.Style(self)
        s.configure("Message.TLabel", font=("Arial", fontSize))
        # find good anchor
        if message['info']:
            anchor = CENTER
            msgLabel['background'] = 'white'
            msgLabel['foreground'] = 'black'
            self['background'] = 'white'
            self['foreground'] = 'black'
            self['text'] = 'INFORMATION'
        elif message['distant']:
            anchor = "nw"
        else:
            anchor = "ne"
        self.pack(anchor=anchor, padx=5)
        
    