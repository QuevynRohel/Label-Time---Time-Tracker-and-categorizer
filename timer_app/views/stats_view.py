import tkinter as tk
from views.navigation import navigate_to

class StatsView:
    def __init__(self, root):
        self.root = root
        self.clear_window()
        self.create_stats_view()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_stats_view(self):
        tk.Label(self.root, text="Statistiques (à développer)").pack(pady=20)

        btn_back = tk.Button(self.root, text="Retour", command=lambda: MainMenu(self.root))
        btn_back.place(x=350, y=10)