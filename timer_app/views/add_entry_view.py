import tkinter as tk
import re

try:
    from tkinter import ttk
except ImportError:
    import tkinter.ttk as ttk
from datetime import datetime, timedelta
from controllers.csv_controller import CSVController
from utils.constants import VIEW_MAIN_MENU
from utils.translations import _
from utils.time_utils import format_time
from views.navigation import navigate_to
from datetime import datetime

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
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, date.strftime("%Y-%m-%d"))
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

        # Section Temps avec Spinbox pour HH, MM, SS
        tk.Label(container, text=_("Temps"), font=("Helvetica", 10)).pack(anchor="w", pady=(10, 5))

        time_frame = tk.Frame(container)
        time_frame.pack(fill="x", pady=(10, 5))

        # Configuration du grid pour créer un espacement type "space-between"
        time_frame.columnconfigure(0, weight=1)  # Espacement à gauche
        time_frame.columnconfigure(2, weight=1)  # Espacement entre heures et minutes
        time_frame.columnconfigure(4, weight=1)  # Espacement entre minutes et secondes
        time_frame.columnconfigure(6, weight=1)  # Espacement à droite

        # Spinbox pour les heures
        self.hours_spinbox = tk.Spinbox(time_frame, from_=0, to=23, width=3, font=("Helvetica", 12), format="%02.0f", relief="flat")
        self.hours_spinbox.grid(row=0, column=1, padx=(10, 10), sticky="ew")
        tk.Label(time_frame, text="h", font=("Helvetica", 12)).grid(row=0, column=2, padx=(5, 5), sticky="ew")

        # Spinbox pour les minutes
        self.minutes_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=3, font=("Helvetica", 12), format="%02.0f", relief="flat")
        self.minutes_spinbox.grid(row=0, column=3, padx=(10, 10), sticky="ew")
        tk.Label(time_frame, text="min", font=("Helvetica", 12)).grid(row=0, column=4, padx=(5, 5), sticky="ew")

        # Spinbox pour les secondes
        self.seconds_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=3, font=("Helvetica", 12), format="%02.0f", relief="flat")
        self.seconds_spinbox.grid(row=0, column=5, padx=(10, 10), sticky="ew")
        tk.Label(time_frame, text="sec", font=("Helvetica", 12)).grid(row=0, column=6, padx=(5, 5), sticky="ew")


        # Section Catégorie accomplie et entrée pour catégorie
        tk.Label(container, text=_("Catégorie accomplie"), font=("Helvetica", 10)).pack(anchor="w", pady=(30, 5))
        category_entry = tk.Entry(container, textvariable=self.category, width=40, font=("Helvetica", 12), relief="flat", highlightbackground="#ddd", highlightthickness=1)
        category_entry.pack(fill="x", padx=10, pady=5)

        # Boutons pour les catégories existantes
        self.load_category_buttons(container)

        # Ligne de la date et heure, centrée avec style de bouton
        tk.Label(container, text=_("Date"), font=("Helvetica", 10)).pack(anchor="w", pady=(30, 5))

        datetime_frame = tk.Frame(container, relief="flat", padx=5, pady=5)
        datetime_frame.pack(fill="x", pady=(10, 5))

        # Frame intermédiaire pour centrer la ligne de date et heure
        datetime_centered_frame = tk.Frame(datetime_frame)
        datetime_centered_frame.pack(anchor="center")

        # Contenu de la ligne de date

        tk.Label(datetime_centered_frame, text=_("Le"), font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
        self.date_entry = tk.Entry(datetime_centered_frame, width=15, font=("Helvetica", 12), relief="flat", highlightbackground="#ddd", highlightthickness=1)
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_entry.insert(0, current_date)
        self.date_entry.grid(row=0, column=1, padx=(5, 10))

        # Contenu de l'heure
        tk.Label(datetime_centered_frame, text=_(" à "), font=("Helvetica", 12)).grid(row=0, column=2, sticky="w")
        self.time_picker = tk.Spinbox(datetime_centered_frame, from_=0, to=23, width=3, font=("Helvetica", 12), format="%02.0f", relief="flat", highlightbackground="#ddd", highlightthickness=1)
        self.time_picker.grid(row=0, column=3, padx=(5, 10))

        tk.Label(datetime_centered_frame, text=_("h"), font=("Helvetica", 12)).grid(row=0, column=4, sticky="w")
        self.minute_picker = tk.Spinbox(datetime_centered_frame, from_=0, to=59, width=3, font=("Helvetica", 12), format="%02.0f", relief="flat", highlightbackground="#ddd", highlightthickness=1)
        self.minute_picker.grid(row=0, column=5, padx=(5, 10))

        # Bouton pour définir des dates rapides
        date_buttons_frame = tk.Frame(container)
        date_buttons_frame.pack(fill="x", pady=(10, 5))

        date_buttons_centered_frame = tk.Frame(date_buttons_frame)
        date_buttons_centered_frame.pack(anchor="center")

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
        existing_categories = CSVController().get_categories()
        if existing_categories:
            categories_frame = tk.Frame(container)
            categories_frame.pack(pady=10)
            for cat in existing_categories:
                btn = tk.Button(categories_frame, text=cat, command=lambda c=cat: self.category.set(c), font=("Helvetica", 10), bg="#ddd", fg="#333", activebackground="#ccc", relief="flat", padx=10, pady=5, cursor="hand2")
                btn.pack(side="left", padx=5)

  

    def validate_date(self, date_text):
        """Valide et formate la date selon la locale."""
        
        # International date format (output)
        formats_intl = "%Y-%m-%d"
        
        # Regex to match various date formats (dd/mm/yyyy, dd-mm-yyyy, dd mm yyyy, yyyy-mm-dd)
        date_pattern = r"(\d{2,4})[\/\-\s](\d{2})[\/\-\s](\d{2,4})"
        
        match = re.match(date_pattern, date_text)
        print(match)
        if match:
            year, month, day = match.groups() # can be day, month, year.
            if len(year) == 4:
                try:
                    parsed_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")

                except ValueError:
                    return None
            else:
                try:
                    parsed_date = datetime.strptime(f"{day}-{month}-{year}", "%Y-%m-%d")
                except ValueError:
                    return None

            return parsed_date.strftime(formats_intl)
        
        print("Error while formatting date:", date_text)
        return None


    def set_date_offset(self, days):
        target_date = datetime.now() + timedelta(days=days)
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, target_date.strftime("%Y-%m-%d"))
        self.time_picker.delete(0, "end")
        self.time_picker.insert(0, target_date.strftime("%H"))
        self.minute_picker.delete(0, "end")
        self.minute_picker.insert(0, target_date.strftime("%M"))

    def set_to_now(self):
        now = datetime.now()
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, now.strftime("%Y-%m-%d"))
        self.time_picker.delete(0, "end")
        self.time_picker.insert(0, now.strftime("%H"))
        self.minute_picker.delete(0, "end")
        self.minute_picker.insert(0, now.strftime("%M"))

    def save_entry(self, description):
        try:
            hours = int(self.hours_spinbox.get())
            minutes = int(self.minutes_spinbox.get())
            seconds = int(self.seconds_spinbox.get())
            total_seconds = hours * 3600 + minutes * 60 + seconds

            date_text = self.date_entry.get().strip()
            valid_date = self.validate_date(date_text)

            date_hour = int(self.hours_spinbox.get())
            date_minute = int(self.minutes_spinbox.get())
            date_second = 0

            print(valid_date)
            if not valid_date:
                self.show_message(_("Date invalide, veuillez vérifier le format.") + " "+ date_text, "red")
                return
            
            entry_date = f"{valid_date} {date_hour:02}:{date_minute:02}:{date_second:02}"
            print("Entry Date:", entry_date)

            if not self.category.get():
                self.show_message(_("Veuillez entrer une catégorie."), "red")
                return

            if total_seconds <= 0:
                self.show_message(_("Le temps doit être supérieur à zéro."), "red")
                return

            CSVController().save_entry(self.category.get(), description, total_seconds, entry_date)
            self.show_message(_("Temps de {} sur '{}' enregistré avec succès !").format(format_time(total_seconds), self.category.get()), "green")
            self.reset_fields()
            navigate_to(self.root, VIEW_MAIN_MENU)

        except ValueError:
            self.show_message(_("Le temps doit être un nombre valide."), "red")

    def show_message(self, message, color):
        self.message_label.config(text=message, fg=color)
        self.root.after(5000, lambda: self.message_label.config(text=""))

    def reset_fields(self):
        self.category.set("")
        self.hours_spinbox.delete(0, "end")
        self.hours_spinbox.insert(0, "00")
        self.minutes_spinbox.delete(0, "end")
        self.minutes_spinbox.insert(0, "00")
        self.seconds_spinbox.delete(0, "end")
        self.seconds_spinbox.insert(0, "00")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.time_picker.delete(0, "end")
        self.time_picker.insert(0, "00")
        self.minute_picker.delete(0, "end")
        self.minute_picker.insert(0, "00")
