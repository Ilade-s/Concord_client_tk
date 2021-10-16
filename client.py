"""
Interface client en tkinter de la messagerie instantanée Concord
"""
from tkinter import *
from tkinter import ttk
# Frames individuelles
from NavBar import *
from ContentFrame import *
from MenuBar import *

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
        self.iconphoto(True, PhotoImage(file="assets/logo.png"))
        self.title(
            f"Concord client v{__VERSION__}")
        self.geometry("{}x{}".format(x, y))
        self.setup_frames()

    def setup_frames(self):
        """
        Place les Frames dans la grille
        """
        self.navBar = NavBar(self)
        self.contentFrame = ContentFrame(self)
        self.bind('<MouseWheel>', self.contentFrame.scroll_msgs)
        self.Menu = MenuBar(self)
        self.config(menu=self.Menu)

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