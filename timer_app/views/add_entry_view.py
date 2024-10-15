import tkinter as tk
from tkinter import ttk
from datetime import datetime
from controllers.csv_controller import CSVController
from utils.constants import VIEW_MAIN_MENU
from utils.translations import _
from views.navigation import navigate_to

class AddEntryView:
    def __init__(self, root):
        self.root = root
        self.clear_window()
        self.create_add_entry_view()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_add_entry_view(self):
        # Barre de navigation avec bouton Retour
        self.add_navigation_bar()

        # Bandeau de message initialement vide
        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#f5f5f5", fg="black")
        self.message_label.pack(fill="x")

        # Conteneur centré
        container = tk.Frame(self.root, bg="#f5f5f5")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text=_("Ajouter une entrée"), font=("Helvetica", 16)).pack(pady=10)

        # Champs pour les détails de l'entrée
        self.category = tk.StringVar()
        self.description = tk.StringVar()
        self.session_seconds = tk.StringVar(value="0")
        self.time_unit = tk.StringVar(value="seconds")  # Par défaut en secondes

        # Champ de Catégorie
        tk.Label(container, text=_("Catégorie"), font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="center", pady=(10, 5))
        category_entry = tk.Entry(container, textvariable=self.category, width=40, font=("Helvetica", 12))
        category_entry.pack(pady=5)

        # Tableau des catégories existantes
        self.load_category_buttons(container)

        # Champ de Description
        tk.Label(container, text=_("Description"), font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="center", pady=(10, 5))
        description_entry = tk.Text(container, width=40, height=4, font=("Helvetica", 12))
        description_entry.pack(pady=5)

        # Sélecteur de Date et Heure
        tk.Label(container, text=_("Date et Heure"), font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="center", pady=(10, 5))
        date_entry = tk.Entry(container, width=20, font=("Helvetica", 12))
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        date_entry.pack(pady=5)

        # Champ de Temps et Radio Boutons pour les unités
        tk.Label(container, text=_("Temps en secondes"), font=("Helvetica", 12), bg="#f5f5f5").pack(anchor="center", pady=(10, 5))
        time_entry = tk.Entry(container, textvariable=self.session_seconds, width=10, font=("Helvetica", 12))
        time_entry.pack(pady=5)

        # Radio boutons pour sélectionner les unités de temps
        radio_frame = tk.Frame(container, bg="#f5f5f5")
        tk.Radiobutton(radio_frame, text=_("Secondes"), variable=self.time_unit, value="seconds", bg="#f5f5f5", font=("Helvetica", 10)).pack(side="left", padx=5)
        tk.Radiobutton(radio_frame, text=_("Minutes"), variable=self.time_unit, value="minutes", bg="#f5f5f5", font=("Helvetica", 10)).pack(side="left", padx=5)
        radio_frame.pack(pady=5)

        # Bouton Enregistrer
        btn_save = tk.Button(container, text=_("Enregistrer"), command=lambda: self.save_entry(description_entry.get("1.0", tk.END).strip()), font=("Helvetica", 12), bg="#4a90e2", fg="white", width=20, relief="flat", cursor="hand2")
        btn_save.pack(pady=15)

    def add_navigation_bar(self):
        nav_bar = tk.Frame(self.root, height=40, bg="#e0e0e0")
        nav_bar.pack(fill="x", side="top")
        btn_back = tk.Button(nav_bar, text=_("Retour"), command=lambda: navigate_to(self.root, VIEW_MAIN_MENU), font=("Helvetica", 12), bg="#e0e0e0", relief="flat", activebackground="#dcdcdc", cursor="hand2", highlightthickness=0)
        btn_back.pack(side="right", padx=10, pady=5)

    def load_category_buttons(self, container):
        # Charger les catégories existantes
        existing_categories = CSVController().get_categories()
        if existing_categories:
            categories_frame = tk.Frame(container, bg="#f5f5f5")
            categories_frame.pack(pady=10)
            for cat in existing_categories:
                btn = tk.Button(categories_frame, text=cat, command=lambda c=cat: self.category.set(c), font=("Helvetica", 10), bg="#ddd", fg="#333", activebackground="#ccc", relief="flat", padx=10, pady=5, cursor="hand2")
                btn.pack(side="left", padx=5)

    def save_entry(self, description):
        # Convertir le temps en secondes si nécessaire
        try:
            time_value = int(self.session_seconds.get())
            if self.time_unit.get() == "minutes":
                time_value *= 60  # Convertir les minutes en secondes

            # Validation des entrées
            if not self.category.get():
                self.show_message(_("Veuillez entrer une catégorie."), "red")
                return
            if not self.validate_date():
                self.show_message(_("Date et Heure invalides."), "red")
                return
            if time_value <= 0:
                self.show_message(_("Le temps doit être supérieur à zéro."), "red")
                return

            # Enregistrement des données
            entry = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Temps en secondes": time_value,
                "Catégorie": self.category.get(),
                "Description": description
            }
            CSVController().save_entry(entry)
            self.show_message(_("Temps de {} sur '{}' enregistré avec succès !").format(format_time(time_value), self.category.get()), "green")

            # Réinitialiser les champs après l'enregistrement
            self.reset_fields()
            navigate_to(self.root, VIEW_MAIN_MENU)

        except ValueError:
            self.show_message(_("Le temps doit être un nombre valide."), "red")

    def validate_date(self):
        """Valider si la date est dans le bon format."""
        try:
            datetime.strptime(self.date_entry.get(), "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    def show_message(self, message, color):
        """Afficher un message dans le bandeau avec une couleur spécifique."""
        self.message_label.config(text=message, fg=color)
        self.root.after(5000, lambda: self.message_label.config(text=""))  # Efface le message après 5 secondes

    def reset_fields(self):
        """Réinitialiser les champs après enregistrement."""
        self.category.set("")
        self.description.set("")
        self.session_seconds.set("0")
        self.time_unit.set("seconds")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))