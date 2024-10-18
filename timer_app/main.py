from tkinter import Tk
from utils.constants import *
from utils.translations import _, initialize_language
from views.navigation import navigate_to

if __name__ == "__main__":
    root = Tk()
    root.title(_("TIME TRACKER"))
    root.minsize(800, 800)
    initialize_language()
    navigate_to(root, VIEW_MAIN_MENU)
    root.mainloop()


    