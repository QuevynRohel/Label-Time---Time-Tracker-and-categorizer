import tkinter as tk
import os
import webbrowser  # To open the folder path
from utils.constants import VIEW_MAIN_MENU, CSV_FILE_PATH, VIEW_OPTIONS
from utils.translations import set_language, _, get_available_languages, get_language, get_original_country_name
from views.navigation import navigate_to

class OptionsView:
    def __init__(self, root):
        self.root = root
        self.create_options_view()

    def create_options_view(self):
        self.clear_window()
        self.add_navigation_bar()

        # Conteneur pour les options
        container = tk.Frame(self.root, bg="#f5f5f5")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # # Boutons d'options supplémentaires
        # self.add_option_buttons(container)

        # # Label pour le sélecteur de langue
        tk.Label(container, text=_("Langues"), font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="center", pady=(20, 5))

        # Dropdown for language selection
        languages = get_available_languages()
        # Display the current language with a down arrow (▼) at the end
        lang_menu = tk.Menubutton(container, text=f"{get_original_country_name(get_language())} ▼", relief="flat", 
                                  bg="#f5f5f5", font=("Helvetica", 12), cursor="hand2", width=50, anchor="n")

        lang_menu.menu = tk.Menu(lang_menu, tearoff=0)
        lang_menu["menu"] = lang_menu.menu  # Linking the menu

        # Adding each language to the dropdown
        for lang in languages:
            lang_menu.menu.add_command(label=get_original_country_name(lang), command=lambda l=lang: self.change_language(l))
            lang_menu.menu.xposition("1")

        lang_menu.pack(fill="x", pady=10)  # Full width of the container

    def add_navigation_bar(self):
        top_bar = tk.Frame(self.root, height=100, bg="#e0e0e0")
        top_bar.pack(fill="x", side="top")
        
        # Bouton Retour à droite
        btn_back = tk.Button(top_bar, text=_("Retour"), font=("Arial", 16), bg="#e0e0e0", relief="flat", command=lambda: navigate_to(self.root, VIEW_MAIN_MENU), cursor="hand2")
        btn_back.pack(side="right", padx=10, pady=5)

    def add_option_buttons(self, container):
        # Bouton pour télécharger les temps
        btn_download = tk.Button(container, text=_("Télécharger mes temps"), font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat", cursor="hand2")
        btn_download.pack(fill="x", padx=10, pady=10)

        # Bouton pour ouvrir le dossier des temps
        btn_open_folder = tk.Button(container, text=_("Ouvrir le dossier vers mes temps"), font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="flat", cursor="hand2", command=self.open_times_folder)
        btn_open_folder.pack(fill="x", padx=10, pady=10)

    def open_times_folder(self):
        """Ouvre le dossier contenant le fichier CSV."""
        folder_path = os.path.dirname(CSV_FILE_PATH)
        webbrowser.open(folder_path)

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

    def open_language_menu(self):
        """Affiche un menu pour sélectionner une langue avec les drapeaux."""
        languages = get_available_languages()

        lang_menu = tk.Toplevel(self.root)
        lang_menu.title(_("Sélectionner une langue"))
        lang_menu.geometry("300x400")

        for lang in languages:
            # flagounet = fp.display("France")  # Utiliser le drapeau correspondant à la langue
            lang_button = tk.Button(lang_menu, text=lang, font=("Helvetica", 40), relief="flat", cursor="hand2", command=lambda l=lang: self.change_language(l))
            lang_button.pack(fill="x", padx=10, pady=5)

    def get_language_flag(self):
        """Récupère le drapeau correspondant à la langue actuelle."""
        language_code = get_language().upper()

        return language_code
        # return fp.display("France")
        # return countryflag.getflag(language_code)
    
    