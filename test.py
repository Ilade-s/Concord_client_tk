import socket
from threading import Thread

Host = "172.20.10.2"
Port = 5415
pseudo = input("Votre pseudo : ")
#Création du socket
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((Host,Port))

def send():
    while True:
            msg = input()
            msg = f"{pseudo}§{msg}"
            msg = msg.encode('utf-8')
            socket.send(msg)

def recup():
    while True:
        requete_server = socket.recv(500)
        requete_server = requete_server.decode("utf-8")
        posbreak = requete_server.find("§")
        pseudo = requete_server[0:posbreak]
        message = requete_server[posbreak+1:len(requete_server)]
        print(f"{pseudo} >> {message}")

send = Thread(target=send)
get = Thread(target=recup)

send.start()
get.start()