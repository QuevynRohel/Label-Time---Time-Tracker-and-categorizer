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
        # Barre d'options avec une roue crantée en haut à droite
        top_bar = tk.Frame(self.root, height=100)
        top_bar.pack(fill="x", side="top")
        
        # Icône de roue crantée pour accéder aux options
        btn_options = tk.Button(top_bar, text="⚙", font=("Arial", 16), bg="#f5f5f5", relief="flat", command=lambda: navigate_to(self.root, VIEW_OPTIONS), cursor="hand2")
        btn_options.pack(side="right", padx=10, pady=5)

        # Conteneur centré pour les boutons principaux
        container = tk.Frame(self.root)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Texte d'encouragement
        encouragement_label = tk.Label(container, text=_("Accomplissez de grandes choses aujourd'hui !"), font=("Arial", 14), fg="black")
        encouragement_label.pack(pady=10)

        # Gros boutons pour "Statistiques" et "Démarrer une session"
        btn_start_session = tk.Button(container, text=_("⚡ Démarrer une session"), font=("Arial", 14), width=40, height=2, bg="#4a90e2", fg="white", relief="flat", cursor="hand2")
        btn_start_session.pack(pady=10)
        btn_start_session.config(command=lambda: navigate_to(self.root, VIEW_SESSION))

        btn_stats = tk.Button(container, text=_("📊 Statistiques"), font=("Arial", 14), width=40, height=2, bg="#4a90e2", fg="white", relief="flat", cursor="hand2")
        btn_stats.pack(pady=10)
        btn_stats.config(command=lambda: navigate_to(self.root, VIEW_STATS))
        # Bouton flottant en bas à droite pour "Ajouter une entrée"
        btn_add_entry = tk.Button(self.root, text="+", font=("Arial", 30, "bold"), bg="#27ae60", fg="white", relief="flat", width=4, height=2, cursor="hand2", borderwidth=0)
        btn_add_entry.config(command=lambda: navigate_to(self.root, VIEW_ADD_ENTRY))
        
        # Ajout d'une bordure blanche ronde au bouton "+", placé en bas à droite
        btn_add_entry.place(relx=0.9, rely=0.9, anchor="center")
        btn_add_entry.config(highlightbackground="white", highlightthickness=10)

