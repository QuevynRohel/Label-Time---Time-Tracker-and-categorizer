import tkinter as tk
import time
from controllers.csv_controller import CSVController
from utils.constants import VIEW_MAIN_MENU
from views.navigation import navigate_to

class SessionView:
    def __init__(self, root):
        self.root = root
        self.category = tk.StringVar()
        self.description = tk.StringVar()
        self.timer_running = False
        self.elapsed_time = 0
        self.create_session_view()

    def create_session_view(self):
        self.clear_window()
        self.add_navigation_bar()

        # Style global
        bg_color = "#f5f5f5"
        btn_color = "#4CAF50"
        self.root.configure(bg=bg_color)

        # Conteneur centré pour les éléments principaux
        container = tk.Frame(self.root, bg=bg_color)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Minuterie avec style moderne
        timer_frame = tk.Frame(container, bd=2, relief="groove", bg="white", padx=20, pady=10)
        self.timer_label = tk.Label(timer_frame, text="0:00:00", font=("Helvetica", 36, "bold"), fg="#333", bg="white")
        self.timer_label.pack(pady=10)
        timer_frame.pack(pady=(0, 20), fill="x", padx=20, anchor="center")

        # Conteneur pour les boutons Play/Pause et Stop côte à côte avec styles
        button_frame = tk.Frame(container, bg=bg_color)
        button_frame.pack(anchor="center")

        self.btn_play_pause = tk.Button(
            button_frame, text="\u25B6 Play", command=self.toggle_timer, state="disabled",
            font=("Helvetica", 14), fg="white", bg=btn_color, activebackground="#45a049",
            relief="flat", width=8, padx=5, pady=5, cursor="hand2"
        )
        self.btn_play_pause.grid(row=0, column=0, padx=(0, 10))

        self.btn_stop = tk.Button(
            button_frame, text="\u25A0 Stop", command=self.stop_timer, state="disabled",
            font=("Helvetica", 14), fg="white", bg="#f44336", activebackground="#e53935",
            relief="flat", width=8, padx=5, pady=5, cursor="hand2"
        )
        self.btn_stop.grid(row=0, column=1)

        # Champs "Catégorie" et "Description" en bas avec style moderne
        tk.Label(container, text="Catégorie", font=("Helvetica", 12), bg=bg_color).pack(anchor="center", pady=(20, 5))
        category_entry = tk.Entry(container, textvariable=self.category, width=50, font=("Helvetica", 12))
        category_entry.pack(pady=5)
        
        # Activer le bouton Play dès que l'utilisateur tape dans le champ
        category_entry.bind("<KeyRelease>", self.check_category_entry)

        # Chargement des boutons de catégories existantes
        self.load_category_buttons(container)

        tk.Label(container, text="Description", font=("Helvetica", 12), bg=bg_color).pack(anchor="center", pady=(20, 5))
        description_entry = tk.Text(container, width=50, height=4, font=("Helvetica", 12))
        description_entry.pack(pady=5)

    def add_navigation_bar(self):
        nav_bar = tk.Frame(self.root, height=30, bg="#e0e0e0")
        nav_bar.pack(fill="x", side="top")

        btn_back = tk.Button(nav_bar, text="Retour", command=lambda: navigate_to(self.root, VIEW_MAIN_MENU))
        btn_back.pack(side="right", padx=10)

    def load_category_buttons(self, container):
        # Chargement des catégories existantes avec bouton
        controller = CSVController()
        categories_frame = tk.Frame(container, bg="#f5f5f5")
        categories_frame.pack(pady=10)

        for cat in controller.get_categories():
            btn = tk.Button(
                categories_frame, text=cat, command=lambda c=cat: self.select_category(c),
                font=("Helvetica", 10), bg="#ddd", fg="#333", activebackground="#ccc",
                relief="flat", padx=10, pady=5, cursor="hand2"
            )
            btn.pack(side="left", padx=5)

    def select_category(self, category):
        # Sélectionne la catégorie et active le bouton Play
        self.category.set(category)
        self.check_category_entry(None)

    def check_category_entry(self, event):
        # Active le bouton Play dès qu'une catégorie est entrée
        if self.category.get():
            self.btn_play_pause.config(state="normal")
        else:
            self.btn_play_pause.config(state="disabled")

    def toggle_timer(self):
        # Toggle entre Play et Pause
        if not self.timer_running:
            self.start_time = time.time() - self.elapsed_time
            self.update_timer()
            self.timer_running = True
            self.btn_stop.config(state="normal")
            self.btn_play_pause.config(text="\u23F8 Pause")  # Icône Pause
        else:
            self.root.after_cancel(self.timer_update)
            self.timer_running = False
            self.btn_play_pause.config(text="\u25B6 Play")  # Icône Play

    def update_timer(self):
        self.elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=self.format_time(self.elapsed_time))
        self.timer_update = self.root.after(1000, self.update_timer)

    def stop_timer(self, description=None):
        if self.timer_running:
            self.root.after_cancel(self.timer_update)
        self.timer_running = False
        if description is None:
            description = self.description.get()
        CSVController().save_entry(self.category.get(), description, int(self.elapsed_time))
        self.reset_fields()

    def reset_fields(self):
        self.elapsed_time = 0
        self.timer_label.config(text="0:00:00")
        self.category.set("")
        self.description.set("")
        self.btn_stop.config(state="disabled")
        self.btn_play_pause.config(state="disabled", text="\u25B6 Play")

    def format_time(self, seconds):
        hours, rem = divmod(seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{int(hours)}:{int(minutes):02}:{int(seconds):02}"

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()