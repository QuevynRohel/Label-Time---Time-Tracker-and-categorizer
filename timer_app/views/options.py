import tkinter as tk
from utils.constants import VIEW_MAIN_MENU, VIEW_OPTIONS
from utils.translations import set_language, _, get_available_languages
from views.navigation import navigate_to

class OptionsView:
    def __init__(self, root):
        self.root = root
        self.selected_language = tk.StringVar(value=_("Français") if _("locale") == "fr" else _("Anglais"))
        self.create_options_view()

    def create_options_view(self):
        self.clear_window()
        self.add_navigation_bar()

        # Conteneur pour les options
        container = tk.Frame(self.root, bg="#f5f5f5")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Boutons d'options supplémentaires
        self.add_option_buttons(container)

        # Label pour le sélecteur de langue
        tk.Label(container, text=_("Langues"), font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="center", pady=(20, 5))

        # Liste déroulante pour sélectionner la langue
        languages = get_available_languages()
        lang_menu = tk.Menubutton(container, text=self.selected_language.get(), relief="flat", bg="#f5f5f5", font=("Helvetica", 12), cursor="hand2")
        lang_menu.menu = tk.Menu(lang_menu, tearoff=0)
        lang_menu["menu"] = lang_menu.menu
        for lang in languages:
            lang_menu.menu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        lang_menu.pack(pady=10)

    def add_navigation_bar(self):
        top_bar = tk.Frame(self.root, height=100, bg="#e0e0e0")
        top_bar.pack(fill="x", side="top")
        
        # Bouton Retour
        btn_back = tk.Button(top_bar, text=_("Retour"), font=("Arial", 16), bg="#e0e0e0", relief="flat", command=lambda: navigate_to(self.root, VIEW_MAIN_MENU), cursor="hand2")
        btn_back.pack(side="left", padx=10, pady=5)
        
        # Icône roue crantée
        btn_options = tk.Button(top_bar, text="⚙", font=("Arial", 16), bg="#e0e0e0", relief="flat", command=lambda: navigate_to(self.root, VIEW_OPTIONS), cursor="hand2")
        btn_options.pack(side="right", padx=10, pady=5)

    def add_option_buttons(self, container):
        # Bouton pour télécharger les temps
        btn_download = tk.Button(container, text=_("Télécharger mes temps"), font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat", cursor="hand2")
        btn_download.pack(fill="x", padx=10, pady=10)

        # Bouton pour ouvrir le dossier des temps
        btn_open_folder = tk.Button(container, text=_("Ouvrir le dossier vers mes temps"), font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat", cursor="hand2")
        btn_open_folder.pack(fill="x", padx=10, pady=10)

    def change_language(self, language):
        """Change la langue et rafraîchit l'interface."""
        set_language(language)
        self.selected_language.set(language)
        self.refresh_interface()

    def refresh_interface(self):
        """Recharge l'interface pour appliquer la nouvelle langue."""
        navigate_to(self.root, VIEW_OPTIONS)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
