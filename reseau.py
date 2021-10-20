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
        self.listclient = []
        self.pseudo = pseudo
        self.waitmessage = []
        self.chat = {0:0}

    def __bind(self,Host,Port, Cons=False):
        """
        Ouvre une connextion en tant que HOTE de celle-ci.
            - Host : ip souhaité
            - Port : port ouvert afin de communiquer
        """

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
            self.listclient.append(new_client)
            if Cons: print(f"Connexion : > {ip}")

        if Cons: print("Fermeture port")
        self.CloseBind()

    def CloseBind(self):
        """
        Ferme la discussion en question en tant que hote.

        [ATTENTION] Ne pas lancer la fonction en tant que client (non hote)
        """
        self.serveurstart = False
        for client in self.listclient:
            client.close()
        self.sock.close()

    def __SendMessageByHote(self):
        while self.serveurstart:
            if not self.waitmessage:
                time.sleep(1)
                continue
            msg = f"{self.pseudo}§{self.waitmessage[0]}"
            codemsg = msg.encode("utf-8")
            self.waitmessage.pop(0)
            for client in self.listclient:
                client.send(codemsg)

    def __SendMessageByClient(self):
        while self.serveurstart:
            if not self.waitmessage:
                time.sleep(1)
                continue
            msg = f"{self.pseudo}§{self.waitmessage[0]}"
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
            else:
                self.SendMessage(envoie,True)

    def __GetMessageByClient(self,Cons=False):
        while self.serveurstart:
            requete_server = self.sock.recv(500)
            requete_server = requete_server.decode("utf-8")
            posbreak = requete_server.find("§")

            pseudo = requete_server[0:posbreak]
            message = requete_server[posbreak+1:len(requete_server)]
            ID = self.chat[0]+1
            TIME = time.strftime('%H:%M', time.localtime())
            self.chat[0] = ID
            self.chat[ID] = {"pseudo":pseudo,"time":TIME,"content":message}
            if Cons: print(f"{pseudo} >> {message}")

    def __GetMessageOfClient(self,client,Cons=False):
        requete_client = client.recv(500) #Recuperation des messages
        requete_client_decode = requete_client.decode('utf-8') #Passage en UTF-8

        #Fractionnage du message
        posbreak = requete_client_decode.find("§")
        pseudo = requete_client_decode[0:posbreak]
        message = requete_client_decode[posbreak+1:len(requete_client_decode)]

        #Stockage du message
        ID = self.chat[0]+1
        TIME = time.strftime('%H:%M', time.localtime())
        self.chat[0] = ID
        self.chat[ID] = {"pseudo":pseudo,"time":TIME,"content":message}
        if Cons: print(f"{pseudo} >> {message}")
        #Envoie du message vers les autres client !
        for newclient in self.listclient:
            if newclient != client:
                newclient.send(requete_client)

    def __GetAllMessageByServer(self,Cons=False):
        while self.serveurstart:
            time.sleep(1)
            for client in self.listclient:
                GetMessage = Thread(target=self.__GetMessageOfClient,args=(client,Cons))
                GetMessage.start()


    def HostMessagerie(self, Host='localhost', Port=6300, Cons=False):

        self.serveurstart = True
        self.__bind(Host,Port,Cons) #Ouverture de la session
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



    

    

if __name__ == "__main__":
    pseudo = input("Votre pseudo : ")
    test = reseau(pseudo=pseudo)

    etat = input("Voulez vous etre Host ou Client (H/C)")
    if etat == "H":
        test.HostMessagerie("172.20.10.2",5415,True)
    else:
        test.ClientMessagerie("172.20.10.2",5415,True)
