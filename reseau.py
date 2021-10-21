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
        self.DicoClient = {} #Liste de tout les clients
        self.pseudo = pseudo
        self.waitmessage = []
        self.chat = {0:0}
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 0

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
            new_client, ip = self.sock.accept()
            GetMessage = Thread(target=self.__GetMessageOfClient,args=(new_client,Cons))
            GetMessage.start()
            if Cons: print(f"Connexion : > {ip}")

        if Cons: print("Fermeture port")
        self.CloseBind()

    def CloseBind(self):
        """
        Ferme la discussion en question en tant que hote.

        [ATTENTION] Ne pas lancer la fonction en tant que client (non hote)
        """
        self.__AddMessageInfo("*WARNING* | L'hote vient de fermer la session.")
        time.sleep(1)
        self.serveurstart = False
        time.sleep(1)
        for cle,element in self.DicoClient.items():
            self.DicoClient[element]["client"].close()
            self.DicoClient.pop(cle)
        self.sock.close()

    def CloseClient(self):
        msg = ("§STOPCLIENT§")
        codemsg = msg.encode("utf-8")
        self.sock.send(codemsg)
        self.SendMessage(f"--> {self.pseudo} s'est déconnecté")
        time.sleep(1)
        self.serveurstart = False
    
    def __AddMessageInfo(self,message):
        ID = self.chat[0]+1
        TIME = time.strftime('%H:%M', time.localtime())
        self.chat[0] = ID
        self.chat[ID] = {"pseudo":"INFO","time":TIME,"content":message, 'distant': True, 'info': True}

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

    def __GetMessageByClient(self,Cons=False):
        while self.serveurstart:
            requete_server = self.sock.recv(500)
            requete_server = requete_server.decode("utf-8")
            a = requete_server.split("§")
            pseudoList = [a[i] for i in range(0, len(a), 2)]
            msgList = [a[i] for i in range(1, len(a), 2)]
            for pseudo, message in zip(pseudoList, msgList):
                if pseudo == "INFO!":
                    self.__AddMessageInfo(message)
                else:
                    ID = self.chat[0]+1
                    TIME = time.strftime('%H:%M', time.localtime())
                    self.chat[0] = ID
                    self.chat[ID] = {"pseudo":pseudo,"time":TIME,"content":message, 'distant': True, 'info': False}
                    if Cons: print(f"{pseudo} >> {message}")

    def __GetMessageOfClient(self,client,Cons=False):
        requete_client = client.recv(500) #Recuperation des messages
        requete_client_decode = requete_client.decode('utf-8') #Passage en UTF-8

        #Stockage du message
        a = requete_client_decode.split("§")
        pseudoList = [a[i] for i in range(0, len(a), 2)]
        msgList = [a[i] for i in range(1, len(a), 2)]
        for pseudo, message in zip(pseudoList, msgList):
            
            if message == "STOPCLIENT":
                for cle,element in self.DicoClient.items():
                    if self.DicoClient[element]["client"] == client:
                        self.DicoClient.pop(cle)
                        client.close()

            elif requete_client_decode == "GETIP":
                pass

            elif pseudo == "CARTEID":
                #Recuperation des deux infos dans le texte
                psd,ip = message.split("|")
                self.DicoClient[ip] = {"pseudo":psd,"client":client}
                #Envoie d'un message a titre INFORMATIF
                self.__AddMessageInfo(f"{psd} viens de se connecter")
            
            else:
                ID = self.chat[0]+1
                TIME = time.strftime('%H:%M', time.localtime())
                self.chat[0] = ID
                self.chat[ID] = {"pseudo":pseudo,"time":TIME,"content":message, 'distant': True, 'info': False}
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
        carte = f"CARTEID§{self.pseudo}|{self.ip}"
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
            - dico[1 à dico[0]] = {'pseudo':''User, 'time': 'hh:mm', 'content' : 'Hey'}
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
        test.ClientMessagerie("172.20.10.2",6300,True)
