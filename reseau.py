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

    def SendMessage(self,message,Cons=False):
        if Cons:print(f"{self.pseudo} >> {message}")
        self.waitmessage.append(str(message))

    def __ConsoleUseSend(self):
        while self.serveurstart:
            envoie = input(f"--------- SEND >> ")
            if envoie == "/stop":
                self.CloseBind()
            else:
                self.SendMessage(envoie,True)

    def __GetMessageOfClient(self,client):
        requete_client = client.recv(500)
        requete_client = requete_client.decode('utf-8')

        posbreak = requete_client.find("§")
        pseudo = requete_client[0:posbreak]
        message = requete_client[posbreak+1:len(requete_client)]

        ID = self.chat[0]+1
        TIME = time.strftime('%H:%M', time.localtime())
        self.chat[0] = ID
        self.chat[ID] = {"pseudo":pseudo,"time":TIME,"content":message}
        print(self.chat)

    def __GetAllMessageByServer(self):
        while self.serveurstart:
            time.sleep(1)
            for client in self.listclient:
                # self.listclient.index(client) = Thread(target=self.__GetMessageOfClient,args=[client])
                # self.listclient.index(client).start
                self.__GetMessageOfClient(client)


    def HostMessagerie(self, Host='localhost', Port=6300, Cons=False):

        self.serveurstart = True
        self.__bind(Host,Port,Cons) #Ouverture de la session
        request = Thread(target=self.__RequestClient,args=[Cons])
        send = Thread(target=self.__SendMessageByHote)
        get = Thread(target=self.__GetAllMessageByServer)
        request.start()
        send.start()
        get.start()
        if Cons: #Utiliser si nous voulons lancer le chat via la console
            console = Thread(target=self.__ConsoleUseSend())
            console.start()


    

if __name__ == "__main__":
    test = reseau()

    test.HostMessagerie("192.168.1.96",5415,True)
