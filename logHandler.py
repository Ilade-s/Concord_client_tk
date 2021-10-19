"""
Handler pour tout ce qui touche aux fichiers de log en json
Permet d'interfacer sans lien direct avec la gui
Sous la forme d'une classe, le construteur ouvre un fichier ou en ouvre un nouveau
"""
import json
from datetime import datetime
import os

class LogHandler:

    def __init__(self, pseudo, is_host) -> None:
        """
        Crée un fichier de log au fromat de nom AAAA-MM-JJ(-n si plusieurs dans la journée)

        STRUCTURE JSON (clés) :
        -----------
            - pseudo : nom choisi pour la discussion (str)
            - creation : heure (HH:MM) de création du fichier (str)
            - is_host : informe si ce client était hôte ou invité (bool)
            - members : autres membres de la discussion (dict[ip: pseudo]) (vide au départ)
            - messages : liste des messages envoyés, sous la forme de dictionnaire (list[msg: dict])

        PARAMETRES :
        -----------
            - pseudo : str
            - is_host : bool
        """
        initalDict = {
            'pseudo': pseudo,
            'creation_time': datetime.now().strftime('%H:%M'),
            'is_host': is_host,
            'members': {},
            'messages': [],

        }
        path = f'logs/{datetime.today().strftime("%Y-%m-%d")}.json'
        if os.path.exists(path):
            i = 0
            pathAlt = path
            while os.path.exists(pathAlt):
                i += 1
                pathAlt = path.split('.')[0] + f'_{i}.json'
            path = pathAlt

        with open(path, 'x+') as file:
            json.dump(initalDict, file)

        with open(path, 'r+') as file:
            self.content = json.load(file)
        
        self.path = path
    
    def update_content(self):
        with open(self.path, 'r+') as file:
            self.content = json.load(file)
    
    def edit_pseudo(self, new_pseudo):
        self.content['pseudo'] = new_pseudo
        self.commit()
    
    def add_member(self, name, ip):
        self.content['members'][ip] = name
        self.commit()
    
    def add_message(self, msg):
        """msg is the dictionary with this format"""
        self.content['messages'].append(msg)
        self.commit()
    
    def commit(self):
        """update the log file with new data from self.content"""
        with open(self.path, 'w+') as file:
            json.dump(self.content, file)


if __name__ == '__main__':
    handler = LogHandler('ilade', True)
        