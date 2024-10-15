import tkinter as tk
from views.navigation import navigate_to
from utils.constants import VIEW_STATS, VIEW_ADD_ENTRY, VIEW_SESSION, VIEW_OPTIONS
from utils.translations import _

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.clear_window()
        self.create_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        tk.Label(self.root, text=_("TIME TRACKER"), font=("Arial", 16)).pack(pady=10)

        btn_stats = tk.Button(self.root, text=_("Statistiques"), command=lambda: navigate_to(self.root, VIEW_STATS))
        btn_stats.pack(pady=10)

        btn_add_entry = tk.Button(self.root, text=_("Ajouter une entrée"), command=lambda: navigate_to(self.root, VIEW_ADD_ENTRY))
        btn_add_entry.pack(pady=10)

        btn_start_session = tk.Button(self.root, text=_("Démarrer une session"), command=lambda: navigate_to(self.root, VIEW_SESSION))
        btn_start_session.pack(pady=10)

        # Bouton pour accéder aux options
        btn_options = tk.Button(self.root, text=_("Options"), command=lambda: navigate_to(self.root, VIEW_OPTIONS))
        btn_options.pack(pady=10)