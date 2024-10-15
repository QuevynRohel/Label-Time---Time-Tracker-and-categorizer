import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chronomètre")
        self.root.minsize(400, 600)

        # Variables
        self.category = tk.StringVar()
        self.description = tk.StringVar()
        self.session_seconds = tk.StringVar(value="0")
        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.categories = set()

        # Charger les catégories depuis le fichier CSV
        self.load_categories()

        # Afficher la vue du menu principal
        self.main_menu_view()

    def load_categories(self):
        try:
            with open("times.csv", "r", newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if reader.fieldnames is None:
                    self.write_csv_headers()
                for row in reader:
                    self.categories.add(row["Catégorie"])
        except FileNotFoundError:
            self.write_csv_headers()

    def write_csv_headers(self):
        with open("times.csv", "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Temps en secondes", "Catégorie", "Description"])

    def main_menu_view(self):
        self.clear_window()

        tk.Label(self.root, text="Chronomètre", font=("Arial", 16)).pack(pady=10)

        btn_stats = tk.Button(self.root, text="Statistiques", command=self.stats_view)
        btn_stats.pack(pady=10)

        btn_add_entry = tk.Button(self.root, text="Ajouter une entrée", command=self.add_entry_view)
        btn_add_entry.pack(pady=10)

        btn_start_session = tk.Button(self.root, text="Démarrer une session", command=self.start_session_view)
        btn_start_session.pack(pady=10)

    def stats_view(self):
        self.clear_window()

        tk.Label(self.root, text="Statistiques (à développer)").pack(pady=20)

        btn_back = tk.Button(self.root, text="Retour", command=self.main_menu_view)
        btn_back.place(x=350, y=10)

    def add_entry_view(self):
        self.clear_window()

        tk.Label(self.root, text="Ajouter une entrée").pack(pady=10)

        tk.Label(self.root, text="Catégorie").pack(anchor="w", padx=20)
        category_entry = tk.Entry(self.root, textvariable=self.category, width=40)
        category_entry.pack(pady=5)

        tk.Label(self.root, text="Description").pack(anchor="w", padx=20)
        description_entry = tk.Text(self.root, width=40, height=4)
        description_entry.pack(pady=5)
        
        tk.Label(self.root, text="Date et Heure").pack(anchor="w", padx=20)
        current_datetime = datetime.now()
        date_entry = tk.Entry(self.root, width=20)
        date_entry.insert(0, current_datetime.strftime("%Y-%m-%d %H:%M"))
        date_entry.pack(pady=5)

        tk.Label(self.root, text="Temps en secondes").pack(anchor="w", padx=20)
        time_entry = tk.Entry(self.root, textvariable=self.session_seconds, width=10)
        time_entry.pack(pady=5)

        btn_save = tk.Button(self.root, text="Enregistrer", command=lambda: self.save_entry(description_entry.get("1.0", tk.END).strip()))
        btn_save.pack(pady=10)

        btn_back = tk.Button(self.root, text="Retour", command=self.main_menu_view)
        btn_back.place(x=350, y=10)

    def start_session_view(self):
        self.clear_window()
        
        tk.Label(self.root, text="Catégorie").pack(anchor="w", padx=20)
        category_entry = tk.Entry(self.root, textvariable=self.category, width=40)
        category_entry.pack(pady=5)

        if self.categories:
            tk.Label(self.root, text="Catégories existantes").pack(anchor="w", padx=20)
            for cat in self.categories:
                btn = tk.Button(self.root, text=cat, command=lambda c=cat: self.category.set(c))
                btn.pack(pady=2)

        tk.Label(self.root, text="Description").pack(anchor="w", padx=20)
        description_entry = tk.Text(self.root, width=40, height=4)
        description_entry.pack(pady=5)

        self.timer_label = tk.Label(self.root, text="0:00:00")
        self.timer_label.pack(pady=10)

        if self.categories:
            btn_play_pause = tk.Button(self.root, text="Play", command=self.toggle_timer)
            btn_play_pause.pack(pady=5)
            
            self.btn_stop = tk.Button(self.root, text="Stop", command=lambda: self.stop_timer(description_entry.get("1.0", tk.END).strip()))
            self.btn_stop.pack(pady=5)
            self.btn_stop.config(state="disabled")
        else:
            tk.Label(self.root, text="Ajoutez une catégorie pour démarrer le chronomètre", fg="red").pack(pady=10)

        btn_back = tk.Button(self.root, text="Retour", command=lambda: self.back_to_main_menu(description_entry.get("1.0", tk.END).strip()))
        btn_back.place(x=350, y=10)

    def toggle_timer(self):
        if not self.timer_running:
            self.start_time = time.time() - self.elapsed_time
            self.update_timer()
            self.timer_running = True
            self.btn_stop.config(state="normal")
        else:
            self.root.after_cancel(self.timer_update)
            self.timer_running = False

    def update_timer(self):
        self.elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=self.format_time(self.elapsed_time))
        self.timer_update = self.root.after(1000, self.update_timer)

    def stop_timer(self, description):
        if self.timer_running:
            self.root.after_cancel(self.timer_update)
        self.timer_running = False
        self.save_session(description)
        self.elapsed_time = 0
        self.timer_label.config(text="0:00:00")
        self.category.set("")
        self.description.set("")
        self.btn_stop.config(state="disabled")

    def save_entry(self, description):
        self.save_to_csv(self.category.get(), description, int(self.session_seconds.get()))

    def save_session(self, description):
        self.save_to_csv(self.category.get(), description, int(self.elapsed_time))

    def save_to_csv(self, category, description, elapsed_seconds):
        with open("times.csv", "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), elapsed_seconds, category, description])

        # Update categories
        self.categories.add(category)

    def format_time(self, seconds):
        hours, rem = divmod(seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

    def back_to_main_menu(self, description):
        if self.timer_running:
            self.stop_timer(description)
        self.main_menu_view()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()