"""
Contient la frame qui permettera de donner des informations textuelles quand nécessaires : 
TODO
"""
from tkinter import *
from tkinter import ttk, messagebox as msgbox
from functools import partial
from logHandler import LogHandler

class EventFrame(LabelFrame):
    """
    Frame utilisé pour la récupération d'information textuelles :
        - connexion à un autre client
        - choix de sauvegarde des logs
    située (packée) dans ContentFrame
    """

    def __init__(self, master, goal="connexion", ashost=False):
        """
        Création et affichage de la Frame souhaitée

        params :
            - master : fenêtre maîtresse (sera ContentFrame)
            - goal : str : indique le but de la Frame à afficher (et donc les widgets à ajouter):
                - "connexion" : fenêtre de connexion à un autre client (ip,...)
                - "host": fenêtre pour hosting d'une discussion
            - ashost : bool
        """
        super().__init__(master, background='#7985DF',
                         relief=SOLID, text=f"EventFrame : {goal}")
        self.master = master
        if goal == "connexion":
            self.master.master.host = False
            self.connexionFrame()
        elif goal == "host":
            self.master.master.host = True
            self.hostFrame()
        self.pack(anchor="nw", pady=5, padx=20, expand=True)
    
    def connexionFrame(self):
        def login_attempt(ip, port, pseudo):
            target_ip = ip.get()
            port = int(port.get())
            pseudo = pseudo.get()
            try:
                self.master.master.pseudo = pseudo
                self.master.master.network.ChangePseudo(pseudo)
                self.master.master.network.ClientMessagerie(target_ip, port)

                self.master.master.log = LogHandler(pseudo, False) # create log file
                self.master.master.navBar.infoFrame.update_logLabel(self.master.master.log.get_path())
                self.master.master.navBar.infoFrame.update_connexionLabel(target_ip, False)
                self.master.master.navBar.inputFrame.imgBtn['state'] = NORMAL
                self.master.master.contentFrame.setup_join() # setup content frame for network dicussion
                self.master.master.Menu.hide_connect_menu()
                self.destroy()
            except Exception as e:
                print(f"Echec de la connexion à l'adresse {target_ip}")
                msgbox.showerror(
                    "login Serveur", f"Echec de la connexion à {target_ip}, veuillez réessayer : {e}")

        self["text"] = "Connexion à une salle"
        ip = StringVar()
        pseudo = StringVar()
        ip.set(self.master.master.network.GetIpLocal())

        # Création widgets
        Label(self, text="ip adress :", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        Label(self, text="port :", font=(17), background=self["background"], foreground="white"
              ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        Label(self, text="pseudo :", font=(17), background=self["background"], foreground="white"
              ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        portBox = ttk.Spinbox(self, width=30, background=self["background"], from_=1, to=50000, increment=1.0)
        portBox.set(6300)
        ttk.Button(self, text="Connect", command=partial(login_attempt, ip, portBox, pseudo), width=20
                   ).grid(row=3, column=1, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.destroy, width=20
                   ).grid(row=3, column=0, padx=10, pady=10)
        idEntry = ttk.Entry(self, textvariable=ip, width=30,
                            background=self["background"])
        pseudoEntry = ttk.Entry(self, textvariable=pseudo,
                        width=30, background=self["background"])
        idEntry.grid(row=0, column=1, padx=10, pady=10)
        portBox.grid(row=1, column=1, padx=10, pady=10)
        pseudoEntry.grid(row=2, column=1, padx=10, pady=10)
    
    def hostFrame(self):
        def login_attempt(port, pseudo):
            port = int(port.get())
            pseudo = pseudo.get()
            try:
                self.master.master.pseudo = pseudo
                self.master.master.network.ChangePseudo(pseudo)
                self.master.master.network.HostMessagerie(port)

                self.master.master.log = LogHandler(pseudo, True) # create log file
                self.master.master.navBar.infoFrame.update_logLabel(self.master.master.log.get_path())
                self.master.master.navBar.infoFrame.update_connexionLabel(self.master.master.network.GetIpLocal(), True)
                self.master.master.navBar.inputFrame.imgBtn['state'] = NORMAL
                self.master.master.contentFrame.setup_join() # setup content frame for network dicussion
                self.master.master.Menu.hide_connect_menu()
                self.destroy()
            except Exception as e:
                print(f"Echec du hosting")
                msgbox.showerror(
                    "login Serveur", f"Echec du hosting, veuillez réessayer : {e}")

        self["text"] = "Création de salle"
        pseudo = StringVar()

        # Création widgets
        Label(self, text="port :", font=(17), background=self["background"], foreground="white"
              ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        Label(self, text="pseudo :", font=(17), background=self["background"], foreground="white"
              ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        portBox = ttk.Spinbox(self, width=30, background=self["background"], from_=1, to=50000, increment=1.0)
        portBox.set(6300)
        ttk.Button(self, text="Create", command=partial(login_attempt, portBox, pseudo), width=20
                   ).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.destroy, width=20
                   ).grid(row=2, column=0, padx=10, pady=10)
        pseudoEntry = ttk.Entry(self, textvariable=pseudo,
                        width=30, background=self["background"])
        portBox.grid(row=0, column=1, padx=10, pady=10)
        pseudoEntry.grid(row=1, column=1, padx=10, pady=10)