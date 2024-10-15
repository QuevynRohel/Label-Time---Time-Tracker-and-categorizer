import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from controllers.csv_controller import CSVController
from utils.constants import VIEW_MAIN_MENU
from utils.translations import _
from utils.time_utils import format_time
from views.navigation import navigate_to
from views.style import configure_dateentry_style

class AddEntryView:
    def __init__(self, root, date=None):
        self.root = root
        self.clear_window()
        self.create_add_entry_view()
        if date:
            self.set_date_and_time(date)
        else:
            self.set_to_now()

    def set_date_and_time(self, date):
        """Définit la date et l'heure dans les widgets."""
        self.date_picker.set_date(date)
        self.time_picker.delete(0, "end")
        self.time_picker.insert(0, date.strftime("%H"))
        self.minute_picker.delete(0, "end")
        self.minute_picker.insert(0, date.strftime("%M"))
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_add_entry_view(self):
        # Barre de navigation avec bouton Retour
        self.add_navigation_bar()

        # Bandeau de message initialement vide
        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 12), fg="black")
        self.message_label.pack(fill="x")

        # Conteneur centré
        container = tk.Frame(self.root)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Titre principal
        self.root.title(_("TIME TRACKER") + " - " + _("Ajouter un temps"))

        # Initialiser les variables nécessaires
        self.category = tk.StringVar()
        self.session_seconds = tk.StringVar(value="0")
        self.time_unit = tk.StringVar(value="minutes")  # Par défaut en minutes

        # Champ Temps avec unité de temps
        time_frame = tk.Frame(container)
        time_frame.pack(fill="x", pady=(10, 5))

        time_entry = tk.Entry(time_frame, textvariable=self.session_seconds, width=10, font=("Helvetica", 12), relief="flat", highlightbackground="#ddd", highlightthickness=1)
        time_entry.pack(fill="x", padx=10, pady=(5, 0)) 

        # Menu déroulant pour les unités de temps, stylé comme les boutons de catégories
        unit_selector = ttk.Combobox(time_frame, textvariable=self.time_unit, values=["secondes", "minutes"], state="readonly", font=("Helvetica", 10))
        unit_selector.pack(fill="x", padx=10, pady=5)
        unit_selector.configure(style="TCombobox")

        # Section Catégorie accomplie et entrée pour catégorie
        tk.Label(container, text=_("Catégorie accomplie"), font=("Helvetica", 10)).pack(anchor="w", pady=(10, 5))
        category_entry = tk.Entry(container, textvariable=self.category, width=40, font=("Helvetica", 12), relief="flat", highlightbackground="#ddd", highlightthickness=1)
        category_entry.pack(fill="x", padx=10, pady=5)

        # Boutons pour les catégories existantes
        self.load_category_buttons(container)

        # Ligne de la date et heure, centrée avec style de bouton
        datetime_frame = tk.Frame(container, relief="flat", padx=5, pady=5)
        datetime_frame.pack(fill="x", pady=(10, 5))

        # Frame intermédiaire pour centrer la ligne de date et heure
        datetime_centered_frame = tk.Frame(datetime_frame)
        datetime_centered_frame.pack(anchor="center")

        # Contenu de la ligne de date et heure
        tk.Label(datetime_centered_frame, text=_("Le "), font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
        self.date_picker = DateEntry(datetime_centered_frame, width=12, background='darkblue', foreground='white', font=("Helvetica", 12))
        self.date_picker.set_date(datetime.now())
        self.date_picker.grid(row=0, column=1, padx=(5, 10))

        configure_dateentry_style(self.date_picker)

        tk.Label(datetime_centered_frame, text=_(" à "), font=("Helvetica", 12)).grid(row=0, column=2, sticky="w")
        self.time_picker = tk.Spinbox(datetime_centered_frame, from_=0, to=23, width=3, font=("Helvetica", 12), format="%02.0f", relief="flat", highlightbackground="#ddd", highlightthickness=1)
        self.time_picker.grid(row=0, column=3, padx=(5, 10))

        tk.Label(datetime_centered_frame, text=_("h"), font=("Helvetica", 12)).grid(row=0, column=4, sticky="w")
        self.minute_picker = tk.Spinbox(datetime_centered_frame, from_=0, to=59, width=3, font=("Helvetica", 12), format="%02.0f", relief="flat", highlightbackground="#ddd", highlightthickness=1)
        self.minute_picker.grid(row=0, column=5, padx=(5, 10))

        # Conteneur principal pour les boutons
        date_buttons_frame = tk.Frame(container)
        date_buttons_frame.pack(fill="x", pady=(10, 5))

        # Frame intermédiaire pour centrer les boutons horizontalement
        date_buttons_centered_frame = tk.Frame(date_buttons_frame)
        date_buttons_centered_frame.pack(anchor="center")

        # Ajout des boutons dans le frame centré
        for index, (text, offset) in enumerate([("Avant-hier", -2), ("Hier", -1), ("Maintenant", 0)]):
            command = self.set_to_now if offset == 0 else lambda offset=offset: self.set_date_offset(offset)
            btn = tk.Button(
                date_buttons_centered_frame, text=_(text), command=command,
                font=("Helvetica", 10), bg="#e0e0e0", relief="flat", cursor="hand2", padx=10, pady=5
            )
            btn.grid(row=0, column=index, padx=5, pady=5) 

        # Séparateur
        separator = tk.Frame(container, height=1, bd=0, bg="#e0e0e0")
        separator.pack(fill="x", padx=20, pady=(30, 30))

        # Section Description optionnelle
        tk.Label(container, text=_("Description optionnelle"), font=("Helvetica", 10)).pack(anchor="w", pady=(5, 5))
        description_entry = tk.Text(container, width=40, height=4, font=("Helvetica", 12), relief="flat", highlightbackground="#ddd", highlightthickness=1)
        description_entry.pack(fill="x", padx=10, pady=5)

        # Bouton Enregistrer
        btn_save = tk.Button(container, text=_("Enregistrer"), command=lambda: self.save_entry(description_entry.get("1.0", tk.END).strip()), font=("Helvetica", 14, "bold"), bg="#4a90e2", fg="white", width=20, relief="flat", cursor="hand2")
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
            categories_frame = tk.Frame(container)
            categories_frame.pack(pady=10)
            for cat in existing_categories:
                btn = tk.Button(categories_frame, text=cat, command=lambda c=cat: self.category.set(c), font=("Helvetica", 10), bg="#ddd", fg="#333", activebackground="#ccc", relief="flat", padx=10, pady=5, cursor="hand2")
                btn.pack(side="left", padx=5)

    def update_time_label(self, event=None):
        """Mise à jour du label pour les unités de temps selon la sélection."""
        selected_unit = self.time_unit.get()
        label_text = _("Temps en minutes") if selected_unit == "minutes" else _("Temps en secondes")
        self.time_label.config(text=label_text)

    def set_date_offset(self, days):
        """Ajuste la date en fonction d'un décalage en jours."""
        target_date = datetime.now() + timedelta(days=days)
        self.date_picker.set_date(target_date)
        self.time_picker.delete(0, "end")
        self.time_picker.insert(0, target_date.strftime("%H"))
        self.minute_picker.delete(0, "end")
        self.minute_picker.insert(0, target_date.strftime("%M"))
        
    def set_to_now(self):
        """Définit la date, heure et minute aux valeurs actuelles."""
        now = datetime.now()
        self.date_picker.set_date(now)
        self.time_picker.delete(0, "end")
        self.time_picker.insert(0, now.strftime("%H"))
        self.minute_picker.delete(0, "end")
        self.minute_picker.insert(0, now.strftime("%M"))

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
            if time_value <= 0:
                self.show_message(_("Le temps doit être supérieur à zéro."), "red")
                return

            # Enregistrement des données en appelant `save_entry` avec les bons paramètres
            CSVController().save_entry(self.category.get(), description, time_value)
            self.show_message(_("Temps de {} sur '{}' enregistré avec succès !").format(format_time(time_value), self.category.get()), "green")

            # Réinitialiser les champs après l'enregistrement
            self.reset_fields()
            navigate_to(self.root, VIEW_MAIN_MENU)

        except ValueError:
            self.show_message(_("Le temps doit être un nombre valide."), "red")
    
    def show_message(self, message, color):
        """Afficher un message dans le bandeau avec une couleur spécifique."""
        self.message_label.config(text=message, fg=color)
        self.root.after(5000, lambda: self.message_label.config(text=""))

    def reset_fields(self):
        """Réinitialiser les champs après enregistrement."""
        self.category.set("")
        self.session_seconds.set("0")
        self.time_unit.set("minutes")
        self.date_picker.set_date(datetime.now())
        self.time_picker.delete(0, "end")
        self.time_picker.insert(0, "00")
        self.minute_picker.delete(0, "end")
        self.minute_picker.insert(0, "00")