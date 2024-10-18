import tkinter as tk    
import os
import pandas as pd
import random
from datetime import datetime, timedelta
import calendar
from utils.constants import CSV_FILE_PATH, VIEW_MAIN_MENU, VIEW_ADD_ENTRY
from utils.translations import _
from utils.preferences import load_preferences, save_preferences
from utils.time_utils import format_time, format_time_compact, format_time_minimalistic  # Make sure this function is available
from views.navigation import navigate_to
from utils.scrollable_frame import ScrollableFrame

class StatisticsView:
    def __init__(self, root, csv_file=CSV_FILE_PATH):
        self.root = root
        self.csv_file = csv_file
        self.current_date = datetime.now()
        self.categories_colors = load_preferences().get("category_colors", {})
        self.root.minsize(1500, 1000)
        # Configurer la vue pour remplacer l'interface actuelle
        self.root.configure(bg="#f5f5f5")
        self.clear_window()
        
        # Interface principale
        self.add_navigation_bar(self.root)
        self.add_message_label(self.root)

        self.scrollable_frame_class = ScrollableFrame(root)
        self.scrollable_frame = self.scrollable_frame_class.get_frame()
        self.scrollable_frame_class.pack(fill="both", expand=True)

        # for i in range(50):  # Ajout de 50 labels pour tester le scroll
        #     tk.Label(self.scrollable_frame, text=f"Label {i}", bg="#ddffaa").pack()


        self.add_calendar_container(self.scrollable_frame)
        self.add_totals_labels(self.scrollable_frame)
        self.add_summary_table(self.scrollable_frame)

        # # Charger et afficher les statistiques
        self.load_statistics(self.scrollable_frame)
        self.add_page_options_bar(self.root)  # Updated to include the new options bar

    def add_navigation_bar(self, parent):
        # Agrandir la barre du haut (height=100)
        nav_bar = tk.Frame(parent, height=100, bg="#e0e0e0")
        nav_bar.pack(fill="x", side="top")
        btn_back = tk.Button(nav_bar, text=_("Retour"), command=lambda: navigate_to(parent, VIEW_MAIN_MENU),
                             font=("Helvetica", 12), bg="#e0e0e0", relief="flat", activebackground="#dcdcdc",
                             cursor="hand2", highlightthickness=0)
        btn_back.pack(side="right", padx=10, pady=5)

    def add_message_label(self, parent):
        self.message_label = tk.Label(parent, text="", font=("Helvetica", 12), bg="#f5f5f5", fg="black", height=0)
        self.message_label.pack(fill="x")
        

    def add_page_options_bar(self, parent):
        # Nouvelle barre "Option de la page" juste sous la barre de navigation
        options_bar = tk.Frame(parent, height=40)
        options_bar.pack(fill="x", side="bottom", pady=5)

        # Centrer les Frames pour Mois et Année dans options_bar
        options_bar.columnconfigure(0, weight=1)
        options_bar.columnconfigure(3, weight=1)

        # Frame pour Mois
        month_frame = tk.Frame(options_bar, width=30, height=40)
        month_frame.grid(row=0, column=1, padx=10, pady=5)  # Espacement entre les frames

        # Frame pour Année
        year_frame = tk.Frame(options_bar, width=20, height=40)
        year_frame.grid(row=0, column=2, padx=10, pady=5)

        # Boutons pour changer le mois
        btn_prev_month = tk.Button(month_frame, text="\u25C0", command=self.show_previous_month, relief="flat",
                                font=("Helvetica", 18), bg="#d3d3d3", cursor="hand2", borderwidth=0)
        btn_prev_month.pack(side="left")
        self.month_label = tk.Label(month_frame, text=self.current_date.strftime("%B"), font=("Helvetica", 16, "bold"),
                                    width=15, anchor="center")  # Taille de 60px pour le mois
        self.month_label.pack(side="left")
        btn_next_month = tk.Button(month_frame, text="\u25B6", command=self.show_next_month, relief="flat",
                                font=("Helvetica", 18), bg="#d3d3d3", cursor="hand2", borderwidth=0)
        btn_next_month.pack(side="left")

        # Boutons pour changer l'année
        btn_prev_year = tk.Button(year_frame, text="\u25C0", command=self.show_previous_year, relief="flat",
                                font=("Helvetica", 18), bg="#d3d3d3", cursor="hand2", borderwidth=0)
        btn_prev_year.pack(side="left")
        self.year_label = tk.Label(year_frame, text=self.current_date.strftime("%Y"), font=("Helvetica", 16, "bold"),
                                width=10, anchor="center")  # Taille de 40px pour l'année
        self.year_label.pack(side="left")
        btn_next_year = tk.Button(year_frame, text="\u25B6", command=self.show_next_year, relief="flat",
                                font=("Helvetica", 18), bg="#d3d3d3", cursor="hand2", borderwidth=0)
        btn_next_year.pack(side="left")


    def add_calendar_container(self, parent):
        self.calendar_frame = tk.Frame(parent, bg="#f5f5f5")
        self.calendar_frame.pack(padx=10, pady=10)

    def add_totals_labels(self, parent):
        self.total_month_label = tk.Label(parent, text="", font=("Helvetica", 12, "bold"))
        self.total_month_label.pack(pady=10)
        self.total_lifetime_label = tk.Label(parent, text="", font=("Helvetica", 12, "bold"))
        self.total_lifetime_label.pack(pady=10)

    def add_summary_table(self, parent):
        self.summary_frame = tk.Frame(parent, bg="#f5f5f5")
        self.summary_frame.pack(padx=10, pady=(10, 100))

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_statistics(self, parent):
        """Charger et afficher les statistiques à partir du fichier CSV."""
        if not os.path.exists(self.csv_file):
            self.message_label.config(text="Fichier CSV introuvable. Veuillez enregistrer une session d'abord.", fg="red", height=10)
            return

        try:
            df = pd.read_csv(self.csv_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(self.csv_file, encoding='ISO-8859-1')
        except Exception as e:
            self.message_label.config(text=str(e), fg="red", height=10)
            return

        if df is not None:
            df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
            df['Temps en secondes'] = df['Temps en secondes'].astype(float)

            # Ajuster la plage de dates pour inclure les jours qui débordent sur le calendrier
            cal = calendar.Calendar(firstweekday=0)
            month_days = cal.monthdayscalendar(self.current_date.year, self.current_date.month)
            first_week = month_days[0]
            last_week = month_days[-1]

            first_day = min(day for day in first_week if day != 0)
            last_day = max(day for day in last_week if day != 0)

            calendar_start_date = self.current_date.replace(day=first_day)
            calendar_end_date = self.current_date.replace(day=last_day)

            # Inclure les jours des mois précédents et suivants si la semaine déborde
            calendar_start_date -= timedelta(days=7)
            calendar_end_date += timedelta(days=7)

            current_month_data = df[(df['Date'] >= calendar_start_date) & (df['Date'] <= calendar_end_date)]
            self.show_calendar(parent, current_month_data)
            self.calculate_totals(df, current_month_data)
            self.show_summary_table(df, current_month_data)

    def show_calendar(self, parent, current_month_data):
        # Supprimer l'ancien calendrier avant d'en dessiner un nouveau
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Configuration initiale du calendrier
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.current_date.year, self.current_date.month)
        day_frame_width = 150

        # Entêtes des jours de la semaine
        for i, day in enumerate(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]):
            tk.Label(self.calendar_frame, text=day, font=("Helvetica", 12, "bold"), width=15).grid(row=0, column=i)

        # Grouper les données par jour et catégorie
        day_data_grouped = current_month_data.groupby([current_month_data['Date'].dt.date, 'Catégorie'])['Temps en secondes'].sum().reset_index()
        day_descriptions = current_month_data.groupby([current_month_data['Date'].dt.date, 'Catégorie'])['Description'].apply(list).reset_index()

        for row, week in enumerate(month_days, start=1):
            total_week_seconds = 0  # Initialiser le total de la semaine
            for col, day in enumerate(week):
                if day == 0:
                    continue

                date_obj = self.current_date.replace(day=1) + timedelta(days=day - 1)
                day_entries = day_data_grouped[day_data_grouped['Date'] == date_obj.date()]
                total_day_seconds = day_entries['Temps en secondes'].sum()

                # Création du cadre pour chaque jour
                day_frame = tk.Frame(self.calendar_frame, highlightbackground="black", highlightthickness=1,
                                    width=day_frame_width, height=120, bg="white")
                day_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                # Affichage du jour
                day_label = tk.Label(day_frame, text=str(day), font=("Helvetica", 10, "bold"), anchor="nw", bg="white")
                day_label.place(x=5, y=5)
                day_label.bind("<Button-1>", lambda e, current_day=day: self.go_to_add_entry(parent, current_day))

                # Afficher le temps total par jour en haut à droite s'il est supérieur à 0
                if total_day_seconds > 0:
                    total_day_label = tk.Label(day_frame, text=format_time_minimalistic(total_day_seconds), font=("Helvetica", 8, "bold"), fg="#555", anchor="ne", bg="white")
                    total_day_label.place(x=day_frame_width - 10, y=5, anchor="ne")

                # Afficher les catégories et descriptions dans chaque case du jour
                for idx, entry in day_entries.iterrows():
                    category = entry['Catégorie']
                    total_seconds = entry['Temps en secondes']
                    descriptions = day_descriptions[(day_descriptions['Date'] == date_obj.date()) & (day_descriptions['Catégorie'] == category)]
                    if not descriptions.empty:
                        valid_descriptions = [desc for desc_list in descriptions['Description'].values for desc in desc_list if pd.notna(desc) and desc != ""]
                        description_text = "\n".join(valid_descriptions) if valid_descriptions else ""
                    else:
                        description_text = ""

                    # Couleur de la catégorie
                    if category not in self.categories_colors:
                        self.categories_colors[category] = self.generate_random_color()
                    color = self.categories_colors[category]

                    formatted_time = format_time_compact(total_seconds)
                    label = tk.Label(day_frame, text=formatted_time, font=("Helvetica", 14, "bold"), fg=color, bg="white")
                    label.place(x=5, y=30 + list(day_entries.index).index(idx) * 30)

                    if description_text:
                        label.bind("<Enter>", lambda e, text=description_text, border_color=color: self.show_tooltip(parent, e, text, border_color))
                        label.bind("<Leave>", self.hide_tooltip)

                total_week_seconds += total_day_seconds

            # Afficher le total de la semaine à droite
            if total_week_seconds > 0:
                tk.Label(self.calendar_frame, text=format_time_minimalistic(total_week_seconds), font=("Helvetica", 12, "bold")).grid(row=row, column=7, padx=5, pady=5)

        # Sauvegarde des couleurs
        preferences = load_preferences()
        preferences["category_colors"] = self.categories_colors
        save_preferences(preferences)

    def show_tooltip(self, parent, event, text, border_color, text_color="black"):
        if not hasattr(self, "tooltip"):
            self.tooltip = tk.Toplevel(parent)
            self.tooltip.overrideredirect(True)
            inner_frame = tk.Frame(self.tooltip, bg="white", padx=5, pady=5)
            inner_frame.pack(padx=1, pady=1)
            self.tooltip_label = tk.Label(inner_frame, text=text, font=("Helvetica", 10), justify="left", fg=text_color, bg="white")
            self.tooltip_label.pack()

        self.tooltip.config(bg=border_color)
        self.tooltip_label.config(text=text)
        self.tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        self.tooltip.deiconify()

    def hide_tooltip(self, event=None):
        if hasattr(self, "tooltip"):
            self.tooltip.withdraw()

    def go_to_add_entry(self, parent, day):
        selected_date = self.current_date.replace(day=day, hour=12, minute=0)
        navigate_to(parent, VIEW_ADD_ENTRY, date=selected_date)

    def generate_random_color(self):
        colors = ["#FF5733", "#33FF57", "#A833FF", "#FF33A8", "#C866AA", "#33FFF2", "#FF8333", "#8C33FF", "#33FF8C", "#FF3386"]
        return random.choice(colors)

    def calculate_totals(self, df, current_month_data):
        total_seconds_month = current_month_data['Temps en secondes'].sum()
        self.total_month_label.config(text=f"Total pour le mois : {format_time(total_seconds_month)}")
        total_seconds_lifetime = df['Temps en secondes'].sum()
        self.total_lifetime_label.config(text=f"Total pour toute la vie : {format_time(total_seconds_lifetime)}")

    def show_summary_table(self, df, current_month_data):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        monthly_totals = current_month_data.groupby('Catégorie')['Temps en secondes'].sum()
        lifetime_totals = df.groupby('Catégorie')['Temps en secondes'].sum()

        tk.Label(self.summary_frame, text="Catégorie", font=("Helvetica", 14, "bold")).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.summary_frame, text="Temps ce mois-ci", font=("Helvetica", 14, "bold")).grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.summary_frame, text="Temps cumulé", font=("Helvetica", 14, "bold")).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(self.summary_frame, text="Toutes catégories", font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.summary_frame, text=format_time(monthly_totals.sum()), font=("Helvetica", 12, "bold")).grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.summary_frame, text=format_time(lifetime_totals.sum()), font=("Helvetica", 12, "bold")).grid(row=1, column=2, padx=10, pady=5)

        sorted_monthly_totals = monthly_totals.sort_values(ascending=False)
        for i, (category, time_seconds) in enumerate(sorted_monthly_totals.items(), start=2):
            color = self.categories_colors.get(category, "#000000")
            tk.Label(self.summary_frame, text=category, font=("Helvetica", 10), fg=color).grid(row=i, column=0, padx=10, pady=5)
            tk.Label(self.summary_frame, text=format_time(time_seconds), font=("Helvetica", 10), fg=color).grid(row=i, column=1, padx=10, pady=5)
            tk.Label(self.summary_frame, text=format_time(lifetime_totals[category]), font=("Helvetica", 10), fg=color).grid(row=i, column=2, padx=10, pady=5)

    # Ajouter les méthodes pour changer d'année
    def show_previous_year(self):
        self.current_date = self.current_date.replace(year=self.current_date.year - 1)
        self.month_label.config(text=self.current_date.strftime("%B"))
        self.year_label.config(text=self.current_date.strftime("%Y"))
        self.load_statistics(self.scrollable_frame)

    def show_next_year(self):
        self.current_date = self.current_date.replace(year=self.current_date.year + 1)
        self.month_label.config(text=self.current_date.strftime("%B"))
        self.year_label.config(text=self.current_date.strftime("%Y"))
        self.load_statistics(self.scrollable_frame)

    def show_previous_month(self):
        self.current_date = (self.current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        self.month_label.config(text=self.current_date.strftime("%B"))
        self.year_label.config(text=self.current_date.strftime("%Y"))
        self.load_statistics(self.scrollable_frame)

    def show_next_month(self):
        next_month = (self.current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        self.current_date = next_month
        self.month_label.config(text=self.current_date.strftime("%B"))
        self.year_label.config(text=self.current_date.strftime("%Y"))
        self.load_statistics(self.scrollable_frame)
