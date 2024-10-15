import tkinter as tk
from utils.constants import VIEW_MAIN_MENU, VIEW_OPTIONS
from utils.translations import set_language, _, get_available_languages
from views.navigation import navigate_to

class OptionsView:
    def __init__(self, root):
        self.root = root
        self.selected_language = tk.StringVar(value="en")  # Langue par défaut
        self.create_options_view()

    def create_options_view(self):
        self.clear_window()
        self.add_navigation_bar()

        # Conteneur pour les options
        container = tk.Frame(self.root, bg="#f5f5f5")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Label pour le sélecteur de langue
        tk.Label(container, text=_("Langues"), font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="center", pady=(20, 5))

        # Liste déroulante pour sélectionner la langue
        languages = get_available_languages()
        lang_menu = tk.OptionMenu(container, self.selected_language, *languages, command=self.change_language)
        lang_menu.pack(pady=10)

    def add_navigation_bar(self):
        nav_bar = tk.Frame(self.root, height=30, bg="#e0e0e0")
        nav_bar.pack(fill="x", side="top")

        btn_back = tk.Button(nav_bar, text=_("Retour"), command=lambda: navigate_to(self.root, VIEW_MAIN_MENU))
        btn_back.pack(side="right", padx=10)

    def change_language(self, language):
        """Change la langue et rafraîchit l'interface."""
        set_language(language)
        self.refresh_interface()

    def refresh_interface(self):
        """Recharge l'interface pour appliquer la nouvelle langue."""
        navigate_to(self.root, VIEW_OPTIONS)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()