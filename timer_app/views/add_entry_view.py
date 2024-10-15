import tkinter as tk
from datetime import datetime
from controllers.csv_controller import CSVController
from views.main_menu import MainMenu

class AddEntryView:
    def __init__(self, root):
        self.root = root
        self.clear_window()
        self.create_add_entry_view()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_add_entry_view(self):
        tk.Label(self.root, text="Ajouter une entrée").pack(pady=10)
        
        # Fields for entry details
        self.category = tk.StringVar()
        self.description = tk.StringVar()
        self.session_seconds = tk.StringVar(value="0")
        
        # Category field
        tk.Label(self.root, text="Catégorie").pack(anchor="w", padx=20)
        category_entry = tk.Entry(self.root, textvariable=self.category, width=40)
        category_entry.pack(pady=5)

        # Description field
        tk.Label(self.root, text="Description").pack(anchor="w", padx=20)
        description_entry = tk.Text(self.root, width=40, height=4)
        description_entry.pack(pady=5)

        # Date and Time field
        tk.Label(self.root, text="Date et Heure").pack(anchor="w", padx=20)
        date_entry = tk.Entry(self.root, width=20)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M"))
        date_entry.pack(pady=5)

        # Time field
        tk.Label(self.root, text="Temps en secondes").pack(anchor="w", padx=20)
        time_entry = tk.Entry(self.root, textvariable=self.session_seconds, width=10)
        time_entry.pack(pady=5)

        btn_save = tk.Button(self.root, text="Enregistrer", command=lambda: self.save_entry(description_entry.get("1.0", tk.END).strip()))
        btn_save.pack(pady=10)

        btn_back = tk.Button(self.root, text="Retour", command=lambda: MainMenu(self.root))
        btn_back.place(x=350, y=10)

    def save_entry(self, description):
        entry = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Temps en secondes": int(self.session_seconds.get()),
            "Catégorie": self.category.get(),
            "Description": description
        }
        CSVController().save_entry(entry)