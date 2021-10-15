import socket

class reseau:
    """
    Class reseau demandant 1 paramètre :
        - sock : par default : socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """

    def __init__(self, sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        self.sock = sock



test = reseau()