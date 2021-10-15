"""
Contient la frame qui permettera de donner des informations textuelles quand nécessaires : 
TODO
"""
from tkinter import *
from tkinter import ttk

class EventFrame(LabelFrame):
    """
    Frame utilisé pour la récupération d'information textuelles :
        - connexion à un autre client
        - choix de sauvegarde des logs
    située (packée) dans ContentFrame
    """

    def __init__(self, master, goal="connexion"):
        """
        Création et affichage de la Frame souhaitée

        params :
            - master : fenêtre maîtresse (sera ContentFrame)
            - goal : str : indique le but de la Frame à afficher (et donc les widgets à ajouter):
                - "connexion" : fenêtre de connexion à un autre client (ip,...)
                - "log" : fenêtre de récupération des logs
        """
        super().__init__(master, background="#FFB8CD",
                         relief=SOLID, text=f"EventFrame : {goal}")
        self.master = master
        if goal == "connexion":
            self.setup_connexionFrame()
        elif goal == "log":
            self.setup_logFrame()
        self.pack(anchor="nw", pady=5, padx=20, expand=True, ipadx=300, ipady=100)
    
    def setup_connexionFrame(self):
        pass

    def setup_logFrame(self):
        pass