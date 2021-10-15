import socket
from threading import Thread #Permet de faire tourner des fonctions en meme temps (async)

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

    def __SendMessageByHote(self, Cons=False):
        while self.serveurstart:
            if self.waitmessage:
                msg = f"{self.pseudo} >> {self.waitmessage[0]}"
                codemsg = msg.encode("utf-8")
                self.waitmessage.pop(0)
                for client in self.listclient:
                    client.send(codemsg)

    def SendMessage(self,message,Cons=False):
        if Cons:print(f"{self.pseudo} >> {message}")
        self.waitmessage.append(str(message))

    def HostMessagerie(self, Host='localhost', Port=6300, Cons=False):

        self.serveurstart = True
        self.__bind(Host,Port,Cons) #Ouverture de la session
        request = Thread(target=self.__RequestClient,args=[Cons])
        send = Thread(target=self.__SendMessageByHote,args=[Cons])
        request.start()
        send.start()
        test = input(">")
        self.SendMessage(test,Cons)

        
    
    

if __name__ == "__main__":
    test = reseau()

    test.HostMessagerie("192.168.1.96",5415,True)