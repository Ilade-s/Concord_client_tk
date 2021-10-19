"""
Interface client en tkinter de la messagerie instantanée Concord
"""
from tkinter import *
from tkinter import ttk
# Frames individuelles
from NavBar import NavBar
from ContentFrame import ContentFrame
from MenuBar import MenuBar
from logHandler import LogHandler

__AUTHORS__ = 'Raphaël, Matheo and Alban'
__VERSION__ = '0.1'

X = 1000
Y = 600

class TopLevel(Tk):
    """
    Représente le client (l'interface)
    """
    def __init__(self, x=X, y=Y) -> None:
        super().__init__()
        self.version = __VERSION__
        self.authors = __AUTHORS__
        self.pseudo = 'Anon'
        self.host = False
        # TEST --------------
        self.log = LogHandler(self.pseudo, False)
        self.log.add_member('Pedro', '123.145.156.178')
        # TEST --------------
        self.iconphoto(True, PhotoImage(file="assets/logo.png"))
        self.title(
            f"Concord client v{__VERSION__}")
        self.geometry("{}x{}".format(x, y))
        self.__setup_frames()

    def __setup_frames(self):
        """
        Place les Frames dans la grille
        """
        self.contentFrame = ContentFrame(self)
        self.navBar = NavBar(self)
        self.bind('<MouseWheel>', self.contentFrame.scroll_msgs)
        self.Menu = MenuBar(self)
        self.config(menu=self.Menu)
        self.contentFrame.show_last_msg()

def main():
    print("===============================================================")
    print(f"Concord client v{__VERSION__}")
    print(f"Made by {__AUTHORS__}")
    print("Source : https://github.com/Ilade-s/Concord_client_tk")
    print("Assets : https://feathericons.com/")
    print("===============================================================")

    client = TopLevel()
    client.mainloop()

if __name__ == '__main__':
    main()