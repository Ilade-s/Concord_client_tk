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
        self.rendered_msgs = []
        self.msgIndex = 0
        self.__debug_setup()
    
    def scroll_msgs(self, event):
        if (event.num == 5 or event.delta == -120) and self.msgIndex < len(self.msgList) - 1:
            self.msgIndex += 1
        if (event.num == 4 or event.delta == 120) and self.msgIndex > 0:
            self.msgIndex -= 1
        self.render_msgs()

    def __debug_setup(self):
        for _ in range(10):
            self.msgList.append(defaultMessage)
            self.msgList.append(defaultMessage2)
    
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
            msgc = msg.copy()
            msgc['content'] = format_content(msgc['content'], self.get_maxCarac())
            self.rendered_msgs.append(MessageTemplate(self, msgc))
        
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
        
    