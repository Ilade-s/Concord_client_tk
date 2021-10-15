import socket


Host = "192.168.1.96"
Port = 5415

#Création du socket
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((Host,Port))

while True:
    requete_server = socket.recv(500)
    requete_server = requete_server.decode("utf-8")
    print(requete_server)