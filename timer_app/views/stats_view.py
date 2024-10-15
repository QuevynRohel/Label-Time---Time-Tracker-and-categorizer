import tkinter as tk
import os
import pandas as pd
import random
from datetime import datetime, timedelta
import calendar
from utils.constants import CSV_FILE_PATH, VIEW_MAIN_MENU, VIEW_ADD_ENTRY
from utils.translations import _
from utils.preferences import load_preferences, save_preferences
from utils.time_utils import format_time, format_time_compact
from views.navigation import navigate_to

class StatisticsView:
    def __init__(self, root, csv_file=CSV_FILE_PATH):
        self.root = root
        self.csv_file = csv_file
        self.current_date = datetime.now()
        self.categories_colors = load_preferences().get("category_colors", {})

        # Configurer la vue pour remplacer l'interface actuelle
        self.root.configure(bg="#f5f5f5")
        self.clear_window()

        # Interface principale
        self.add_navigation_bar()
        self.add_message_label()
        self.add_month_navigation()
        self.add_calendar_container()
        self.add_totals_labels()
        self.add_summary_table()

        # Charger et afficher les statistiques
        self.load_statistics()

    def add_navigation_bar(self):
        nav_bar = tk.Frame(self.root, height=40, bg="#e0e0e0")
        nav_bar.pack(fill="x", side="top")
        btn_back = tk.Button(nav_bar, text=_("Retour"), command=lambda: navigate_to(self.root, VIEW_MAIN_MENU),
                             font=("Helvetica", 12), bg="#e0e0e0", relief="flat", activebackground="#dcdcdc",
                             cursor="hand2", highlightthickness=0)
        btn_back.pack(side="right", padx=10, pady=5)

    def add_message_label(self):
        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#f5f5f5", fg="black")
        self.message_label.pack(fill="x")

    def add_month_navigation(self):
        button_frame = tk.Frame(self.root, bg="#f5f5f5")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="◄", command=self.show_previous_month, relief="flat",
                  font=("Helvetica", 12), bg="#e0e0e0", cursor="hand2").grid(row=0, column=0, padx=10)
        self.month_label = tk.Label(button_frame, text=self.current_date.strftime("%B %Y"), font=("Helvetica", 16, "bold"))
        self.month_label.grid(row=0, column=1)
        tk.Button(button_frame, text="►", command=self.show_next_month, relief="flat",
                  font=("Helvetica", 12), bg="#e0e0e0", cursor="hand2").grid(row=0, column=2, padx=10)

    def add_calendar_container(self):
        self.calendar_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.calendar_frame.pack(padx=10, pady=10)

    def add_totals_labels(self):
        self.total_month_label = tk.Label(self.root, text="", font=("Helvetica", 12, "bold"))
        self.total_month_label.pack(pady=10)
        self.total_lifetime_label = tk.Label(self.root, text="", font=("Helvetica", 12, "bold"))
        self.total_lifetime_label.pack(pady=10)

    def add_summary_table(self):
        self.summary_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.summary_frame.pack(padx=10, pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_statistics(self):
        """Charger et afficher les statistiques à partir du fichier CSV."""
        if not os.path.exists(self.csv_file):
            self.message_label.config(text="Fichier CSV introuvable. Veuillez enregistrer une session d'abord.", fg="red")
            return

        try:
            df = pd.read_csv(self.csv_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(self.csv_file, encoding='ISO-8859-1')
        except Exception as e:
            self.message_label.config(text=str(e), fg="red")
            return

        if df is not None:
            df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
            df['Temps en secondes'] = df['Temps en secondes'].astype(float)
            month_start = self.current_date.replace(day=1)
            next_month = (month_start + timedelta(days=32)).replace(day=1)
            current_month_data = df[(df['Date'] >= month_start) & (df['Date'] < next_month)]
            self.show_calendar(current_month_data)
            # self.calculate_totals(df, current_month_data)
            self.show_summary_table(df, current_month_data)

    def show_calendar(self, current_month_data):
        # Configuration initiale du calendrier
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.current_date.year, self.current_date.month)
        day_frame_width = 150

        for i, day in enumerate(["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]):
            tk.Label(self.calendar_frame, text=day, font=("Helvetica", 12, "bold"), width=15).grid(row=0, column=i)

        # Grouper les données par jour et catégorie
        day_data_grouped = current_month_data.groupby([current_month_data['Date'].dt.day, 'Catégorie'])['Temps en secondes'].sum().reset_index()
        day_descriptions = current_month_data.groupby([current_month_data['Date'].dt.day, 'Catégorie'])['Description'].apply(list).reset_index()

        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day == 0 or day > calendar.monthrange(self.current_date.year, self.current_date.month)[1]:
                    continue

                day_entries = day_data_grouped[day_data_grouped['Date'] == day]
                day_frame_height = max(120, 30 + 30 * len(day_entries))

                # Création du cadre pour chaque jour
                day_frame = tk.Frame(self.calendar_frame, highlightbackground="black", highlightthickness=1,
                                    width=day_frame_width, height=day_frame_height, bg="white")
                day_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                # Affichage du jour avec cercle en hover
                day_label_size = 10
                day_label = tk.Label(day_frame, text=str(day), font=("Helvetica", day_label_size, "bold"), anchor="nw", bg="white")
                day_label.place(x=5, y=5)
                day_label.bind("<Button-1>", lambda e, current_day=day: self.go_to_add_entry(current_day))
                day_label.bind("<Enter>", lambda e, label=day_label: label.config(font=(("Helvetica", day_label_size + 5, "bold"))))
                day_label.bind("<Leave>", lambda e, label=day_label: label.config(font=(("Helvetica", day_label_size, "bold"))))

                # Récupération des entrées pour chaque jour et catégorie
                
                for _, entry in day_entries.iterrows():
                    category = entry['Catégorie']
                    total_seconds = entry['Temps en secondes']

                    # Récupérer et filtrer les descriptions
                    descriptions = day_descriptions[(day_descriptions['Date'] == day) & (day_descriptions['Catégorie'] == category)]
                    formatted_full_time = format_time(total_seconds)

                    day_descriptions_text = f"{category}: {formatted_full_time}"
                    if not descriptions.empty:
                        valid_descriptions = [desc for desc_list in descriptions['Description'].values for desc in desc_list if pd.notna(desc) and desc != ""]
                        if valid_descriptions:
                            day_descriptions_text = f"{category}: {formatted_full_time}\n\n" + "\n".join(valid_descriptions)

                    # Couleur et format du temps
                    if category not in self.categories_colors:
                        self.categories_colors[category] = self.generate_random_color()
                    color = self.categories_colors[category]

                    # Afficher uniquement les heures en gras
                    formatted_time = format_time_compact(total_seconds)
                    label = tk.Label(day_frame, text=formatted_time, font=("Helvetica", 14, "bold"), fg=color, bg="white")
                    label.place(x=5, y=30 + list(day_entries.index).index(_) * 30)  
                    
                    # Tooltip pour les descriptions
                    label.bind("<Enter>", lambda e, text=day_descriptions_text, border_color=color: self.show_tooltip(e, text, border_color))
                    label.bind("<Leave>", self.hide_tooltip)

        # Sauvegarde des couleurs
        preferences = load_preferences()
        preferences["category_colors"] = self.categories_colors
        save_preferences(preferences)

    def show_tooltip(self, event, text, border_color, text_color="black"):
        if not hasattr(self, "tooltip"):
            self.tooltip = tk.Toplevel(self.root)
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

    def go_to_add_entry(self, day):
        selected_date = self.current_date.replace(day=day, hour=12, minute=0)
        navigate_to(self.root, VIEW_ADD_ENTRY, date=selected_date)

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

    def show_previous_month(self):
        self.current_date = (self.current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        self.month_label.config(text=self.current_date.strftime("%B %Y"))
        self.load_statistics()

    def show_next_month(self):
        next_month = (self.current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        self.current_date = next_month
        self.month_label.config(text=self.current_date.strftime("%B %Y"))
        self.load_statistics()