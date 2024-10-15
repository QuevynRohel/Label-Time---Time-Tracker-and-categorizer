from tkinter import Tk
from utils.constants import *
from utils.translations import _
from views.navigation import navigate_to

if __name__ == "__main__":
    root = Tk()
    root.title(_("TIME TRACKER"))
    root.minsize(800, 800)
    navigate_to(root, VIEW_MAIN_MENU)
    root.mainloop()


    