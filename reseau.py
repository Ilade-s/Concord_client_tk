import socket
from threading import Thread #Permet de faire tourner des fonctions en meme temps (async)
import time

class reseau:
    """
    Class reseau demandant 1 paramètre :
        - sock : par default : socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """

    def __init__(self, sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM), pseudo="User"):
        self.sock = sock
        self.serveurstart = False
        self.DicoClient = {} #Liste de tout les clients ex: {123.456.10.2={« pseudo »:  « banban », « client »:<fonction>}}
        self.pseudo = pseudo
        self.waitmessage = []
        self.chat = {0:0}
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 0
        self.req_incomplete = ()

    def __bind(self,Host,Port, Cons=False):
        """
        Ouvre une connextion en tant que HOTE de celle-ci.
            - Host : ip souhaité
            - Port : port ouvert afin de communiquer
        """
        self.ip = Host
        self.port = Port
        self.sock.bind((Host, Port))
        self.sock.listen(5)
        if Cons: print(f"Ouverture Hote : > {Host} PORT {Port}")

    def __ConnexionMessagerie(self, Host, Port, Cons=False):
        """
        Connexion pour un client
        """
        self.sock.connect((Host,Port))
        if Cons: print(f"Connexion à l'Hote : > {Host} PORT {Port}")
    
    def __RequestClient(self, Cons=False):
        """
        Ouvre une boucle sur intervalle 4.

        Cela attend la connexion d'un nouveau client afin de l'ajouter à la liste des clients.
        """

        while self.serveurstart:
            try:    
                new_client, ip = self.sock.accept()
            except Exception:
                self.__Disconnected_toInterface()
                return 0
            GetMessage = Thread(target=self.__GetMessageOfClient,args=(new_client,Cons))
            GetMessage.start()
            if Cons: print(f"Connexion : > {ip}")

        if Cons: 
            print("Fermeture port")
            self.CloseBind()

    def CloseBind(self):
        """
        Ferme la discussion en question en tant que hote.

        [ATTENTION] Ne pas lancer la fonction en tant que client (non hote)
        """
        self.__AddMessageInfo("*WARNING* | L'hote vient de fermer la session.")
        time.sleep(1)
        self.serveurstart = False
        for element in self.DicoClient.values():
            element["client"].close()
        self.DicoClient = {}
        self.sock.close()

    def CloseClient(self, host_online=True):
        if host_online:
            msg = (f"{self.pseudo}§STOPCLIENT§")
            codemsg = msg.encode("utf-8")
            self.sock.send(codemsg)
            time.sleep(1)
        self.serveurstart = False
        self.chat = {0:0}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def __AddMessageInfo(self,message):
        ID = self.chat[0]+1
        TIME = time.strftime('%H:%M', time.localtime())
        self.chat[0] = ID
        self.chat[ID] = {"pseudo":"INFO","time":TIME,"content":message, 'distant': True, 'info': True, 'error': ''}

        msg = f"INFO!§{message}§"
        codemsg = msg.encode("utf-8")
        for element in self.DicoClient:
            self.DicoClient[element]["client"].send(codemsg)

    def __SendMessageByHote(self):
        while self.serveurstart:
            if not self.waitmessage:
                time.sleep(1)
                continue

            message = self.waitmessage[0]

            if message[0] != '/':
                msg = f"{self.pseudo}§{message}§"
                codemsg = msg.encode("utf-8")
                self.waitmessage.pop(0)
                for element in self.DicoClient:
                    self.DicoClient[element]["client"].send(codemsg)
            else:
                self.waitmessage.pop(0)
                if len(message) >= 3 and message[0:3] == '/ip':
                    pass

    def __SendMessageByClient(self):
        while self.serveurstart:
            if not self.waitmessage:
                time.sleep(1)
                continue
            msg = f"{self.pseudo}§{self.waitmessage[0]}§"
            codemsg = msg.encode("utf-8")
            self.waitmessage.pop(0)
            self.sock.send(codemsg)

    def SendMessage(self,message,Cons=False):
        """
        Fonction qui permet d'envoyer un message.
        Args :
            - message : (str)
        """
        self.waitmessage.append(str(message))

    def __ConsoleUseSend(self):
        while self.serveurstart:
            envoie = input(f"--------- SEND >> ")
            if envoie == "/stop host":
                self.CloseBind()
            elif envoie == "/stop client":
                self.CloseClient()
                print("stop client envoye")
            else:
                self.SendMessage(envoie,True)
    
    def __Disconnected_toInterface(self):
        """sub func called in case __GetMessage fails to fetch the socket
        will add a info message to self.chat to make the interface aware of the deconnection"""
        ID = self.chat[0]+1
        self.chat[0] = ID
        self.chat[ID] = {
            'error': 'DISCONNECTED'
            }

    def __GetMessageByClient(self,Cons=False):
        while self.serveurstart:
            try:
                requete_server = self.sock.recv(10**7)
            except Exception:
                self.__Disconnected_toInterface()
                return 0
            requete_server = requete_server.decode("utf-8")
            a = requete_server.split("§")
            # vérif si message incomplet à la requête précédente
            if self.req_incomplete:
                (type, part) = self.req_incomplete
                if type == 'MSG': # need to add pseudo and concatenate msg part
                    a[0] = part.split('§')[1] + a[0]
                    a.insert(0, part.split('§')[0])
                elif type == 'NAME': # only need to concatenate pseudo part
                    a[0] = part + a[0]
                msg = '§'.join(a[:2])
                self.req_incomplete = ()
                #print(f'completed msg : {msg}')
            # vérif si message incomplet à cette requête
            if a[-1]: # message incomplet
                if (len(a) - 1) % 2: # pseudo complet et message incomplet (= 1 donc index impair)
                    msg = f'{a[-2]}§{a[-1]}'
                    #print(f'incomplete msg : {msg}')
                    self.req_incomplete = ('MSG', msg)
                    a = a[:-2]
                else: # pseudo incomplet et msg manquant (= 0 donc index pair)
                    msg = a[-1]
                    #print(f'incomplete msg : {msg}')
                    self.req_incomplete = ('NAME', msg)
                    a = a[:-1]
            
            print(self.req_incomplete)

            pseudoList = [a[i] for i in range(0, len(a), 2)]
            msgList = [a[i] for i in range(1, len(a), 2)]
            for pseudo, message in zip(pseudoList, msgList):
                if pseudo == "INFO!":
                    self.__AddMessageInfo(message)
                else:
                    ID = self.chat[0]+1
                    TIME = time.strftime('%H:%M', time.localtime())
                    self.chat[0] = ID
                    self.chat[ID] = {
                        "pseudo":pseudo,
                        "time":TIME,
                        "content":message,
                        'distant': True,
                        'info': False,
                        'error': ''
                        }
                    if Cons: print(f"{pseudo} >> {message}")

    def __GetMessageOfClient(self,client,Cons=False):
        try:    
            requete_client = client.recv(10**5) #Recuperation des messages
        except Exception:
            return 0
        requete_client_decode = requete_client.decode('utf-8') #Passage en UTF-8 
        #Stockage du message
        a = requete_client_decode.split("§")
        # vérif si message incomplet à la requête précédente
        if self.req_incomplete:
            (type, part) = self.req_incomplete
            if type == 'MSG': # need to add pseudo and concatenate msg part
                a[0] = part.split('§')[1] + a[0]
                a.insert(0, part.split('§')[0])
            elif type == 'NAME': # only need to concatenate pseudo part
                a[0] = part + a[0]
            msg = '§'.join(a[:2])
            self.req_incomplete = ()
            #print(f'completed msg : {msg}')
        # vérif si message incomplet à cette requête
        if a[-1]: # message incomplet
            if (len(a) - 1) % 2: # pseudo complet et message incomplet (= 1 donc index impair)
                msg = f'{a[-2]}§{a[-1]}'
                #print(f'incomplete msg : {msg}')
                self.req_incomplete = ('MSG', msg)
                a = a[:-2]
            else: # pseudo incomplet et msg manquant (= 0 donc index pair)
                msg = a[-1]
                #print(f'incomplete msg : {msg}')
                self.req_incomplete = ('NAME', msg)
                a = a[:-1]
        
        print(self.req_incomplete)

        pseudoList = [a[i] for i in range(0, len(a), 2)]
        msgList = [a[i] for i in range(1, len(a), 2)]
        for pseudo, message in zip(pseudoList, msgList):
            
            if message == "STOPCLIENT":
                for cle,element in self.DicoClient.copy().items():
                    if element["client"] == client:
                        self.DicoClient.pop(cle)
                        client.close()
                self.__AddMessageInfo(f"{pseudo} s'est déconnecté")

            elif message[:3] == "/ip":
                ippseudo=message.split(" ")
                for cle,element in self.DicoClient.items():
                    if element["pseudo"] == ippseudo[1]:
                        self.SendMessage(cle)

            elif pseudo == "CARTEID":
                #Recuperation des deux infos dans le texte
                psd,ip = message.split("|")
                self.DicoClient[ip] = {"pseudo":psd,"client":client}
                #Envoie d'un message a titre INFORMATIF
                self.__AddMessageInfo(f"{psd} vient de se connecter")
            
            else:
                ID = self.chat[0]+1
                TIME = time.strftime('%H:%M', time.localtime())
                self.chat[0] = ID
                self.chat[ID] = {"pseudo":pseudo,"time":TIME,"content":message, 'distant': True, 'info': False, 'error': ''}
                if Cons: print(f"{pseudo} >> {message}")
                #Envoie du message vers les autres client !
                for element in self.DicoClient:
                    if self.DicoClient[element]["client"] != client:
                        self.DicoClient[element]["client"].send(requete_client)

    def __GetAllMessageByServer(self,Cons=False):
        while self.serveurstart:
            time.sleep(1)
            for element in self.DicoClient:
                GetMessage = Thread(target=self.__GetMessageOfClient,args=(self.DicoClient[element]["client"],Cons))
                GetMessage.start()


    def HostMessagerie(self,Port=6300, Cons=False):

        self.serveurstart = True
        self.__bind(self.ip,Port,Cons) #Ouverture de la session
        request = Thread(target=self.__RequestClient,args=[Cons])
        send = Thread(target=self.__SendMessageByHote)
        get = Thread(target=self.__GetAllMessageByServer,args=[Cons])
        request.start()
        send.start()
        get.start()
        if Cons: #Utiliser si nous voulons lancer le chat via la console
            console = Thread(target=self.__ConsoleUseSend())
            console.start()

    def ClientMessagerie(self, Host='localhost', Port=6300, Cons=False):

        self.serveurstart = True
        self.__ConnexionMessagerie(Host,Port,Cons) #Ouverture de la connexion vers l'hote

        #Envoie cart identite vers le HOST
        carte = f"CARTEID§{self.pseudo}|{self.ip}§"
        codemsg = carte.encode("utf-8")
        self.sock.send(codemsg)

        get = Thread(target=self.__GetMessageByClient,args=[Cons])
        send = Thread(target=self.__SendMessageByClient)
        get.start()
        send.start()

        if Cons: #Utiliser si nous voulons lancer le chat via la console
            console = Thread(target=self.__ConsoleUseSend())
            console.start()

    def FetchMessage(self):
        """
        Retourne un dictionnaire contenant tout les messages reçus.
            - dico[0] = total de message
            - dico[1 à dico[0]] = {'pseudo':''User, 'time': 'hh:mm', 'content' : 'Hey', 'info': bool, 'error': str (vide si pas d'erreur, sinon donne type)}
        [INFO] : La fonction ne retourne pas les propres message de l'utilisateur
        """
        return self.chat

    def ChangePseudo(self,pseudo):
        """
        Permet de modifier le pseudo. 
        La fonction retourne aussi l'ancien pseudo.
        """
        old = self.pseudo
        self.pseudo = pseudo
        return old

    def GetPseudo(self):
        """
        Retourne le pseudo de l'utilisateur.
        """
        return self.pseudo

    def GetInformationConnexion(self):
        """
        Retourne l'ip et le port sous forme de tuple (self.ip,self.port)
        (str | int)
        """
        return(self.ip,self.port)

    def GetIpLocal(self):
        """
        retourne l'ip local
        """
        return self.ip
    

if __name__ == "__main__":
    pseudo = input("Votre pseudo : ")
    test = reseau(pseudo=pseudo)

    etat = input("Voulez vous etre Host ou Client (H/C)")
    if etat == "H":
        test.HostMessagerie(6300,True)
    else:
        test.ClientMessagerie("172.20.10.4",6300,True)
