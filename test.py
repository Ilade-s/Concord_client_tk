import socket


Host = "192.168.1.96"
Port = 5415

#Création du socket
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect((Host,Port))

while True:
        msg = input()
        msg = f"HENRI§{msg}"
        msg = msg.encode('utf-8')
        socket.send(msg)