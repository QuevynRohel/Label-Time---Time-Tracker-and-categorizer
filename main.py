import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")
        
        # Variables
        self.category = tk.StringVar()
        self.description = tk.StringVar()
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
            with open("times.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.categories.add(row["Catégorie"])
        except FileNotFoundError:
            pass

    def main_menu_view(self):
        self.clear_window()

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
        btn_back.pack(pady=10)

    def add_entry_view(self):
        self.clear_window()

        tk.Label(self.root, text="Ajouter une entrée").pack(pady=10)
        
        # Champs d'entrée avec simulation de placeholder
        category_entry = tk.Entry(self.root, textvariable=self.category)
        category_entry.pack(pady=5)
        self.set_placeholder(category_entry, "Catégorie")

        description_entry = tk.Entry(self.root, textvariable=self.description)
        description_entry.pack(pady=5)
        self.set_placeholder(description_entry, "Description")

        btn_save = tk.Button(self.root, text="Enregistrer", command=self.save_entry)
        btn_save.pack(pady=10)

        btn_back = tk.Button(self.root, text="Retour", command=self.main_menu_view)
        btn_back.pack(pady=10)

    def start_session_view(self):
        self.clear_window()
        
        # Champs d'entrée avec simulation de placeholder
        category_entry = tk.Entry(self.root, textvariable=self.category)
        category_entry.pack(pady=5)
        self.set_placeholder(category_entry, "Catégorie")

        description_entry = tk.Entry(self.root, textvariable=self.description)
        description_entry.pack(pady=5)
        self.set_placeholder(description_entry, "Description")

        for cat in self.categories:
            btn = tk.Button(self.root, text=cat, command=lambda c=cat: self.category.set(c))
            btn.pack(pady=2)

        self.timer_label = tk.Label(self.root, text="0:00:00")
        self.timer_label.pack(pady=10)

        btn_play_pause = tk.Button(self.root, text="Play", command=self.toggle_timer)
        btn_play_pause.pack(pady=5)
        
        btn_stop = tk.Button(self.root, text="Stop", command=self.stop_timer)
        btn_stop.pack(pady=5)

        btn_back = tk.Button(self.root, text="Retour", command=self.back_to_main_menu)
        btn_back.pack(pady=10)

    def toggle_timer(self):
        if not self.timer_running:
            self.start_time = time.time() - self.elapsed_time
            self.update_timer()
            self.timer_running = True
        else:
            self.root.after_cancel(self.timer_update)
            self.timer_running = False

    def update_timer(self):
        self.elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=self.format_time(self.elapsed_time))
        self.timer_update = self.root.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_running:
            self.root.after_cancel(self.timer_update)
        self.timer_running = False
        self.save_session()
        self.elapsed_time = 0
        self.timer_label.config(text="0:00:00")
        self.category.set("")
        self.description.set("")

    def save_entry(self):
        self.save_to_csv(self.category.get(), self.description.get(), elapsed_seconds=0)

    def save_session(self):
        self.save_to_csv(self.category.get(), self.description.get(), elapsed_seconds=int(self.elapsed_time))

    def save_to_csv(self, category, description, elapsed_seconds):
        with open("times.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), elapsed_seconds, category, description])

        # Update categories
        self.categories.add(category)

    def format_time(self, seconds):
        hours, rem = divmod(seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

    def back_to_main_menu(self):
        if self.timer_running:
            self.stop_timer()
        self.main_menu_view()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def set_placeholder(self, entry, placeholder_text):
        entry.insert(0, placeholder_text)
        entry.bind("<FocusIn>", lambda event: self.clear_placeholder(entry, placeholder_text))
        entry.bind("<FocusOut>", lambda event: self.restore_placeholder(entry, placeholder_text))

    def clear_placeholder(self, entry, placeholder_text):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)

    def restore_placeholder(self, entry, placeholder_text):
        if not entry.get():
            entry.insert(0, placeholder_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()