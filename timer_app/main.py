from tkinter import Tk
from utils.constants import *
from views.navigation import navigate_to

if __name__ == "__main__":
    root = Tk()
    root.title("TIME TRACKER")
    root.minsize(600, 800)
    navigate_to(root, VIEW_MAIN_MENU)
    root.mainloop()


    