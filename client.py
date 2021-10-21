"""
Interface client en tkinter de la messagerie instantanée Concord
"""
from tkinter import *
from tkinter import ttk, messagebox as msgbox
# Frames individuelles
from NavBar import NavBar
from ContentFrame import ContentFrame
from MenuBar import MenuBar
from reseau import reseau

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
        self.log = None
        self.network = reseau(pseudo=self.pseudo)
        self.iconphoto(True, PhotoImage(file="assets/logo.png"))
        self.title(
            f"Concord client v{__VERSION__}")
        self.geometry("{}x{}".format(x, y))
        self.__setup_frames()

    def __setup_frames(self):
        """
        Place les Frames dans la grille
        """
        def close_window():
            if self.network.serveurstart and msgbox.askyesno('Quit', 'Are you sure you want to quit ?'):
                try:
                    self.contentFrame.stop_update()
                    if self.host:
                        self.network.CloseBind()
                    else:
                        self.network.CloseClient()
                except Exception:
                    pass
                
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", close_window)
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