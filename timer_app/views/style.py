from tkinter import ttk
from tkcalendar import Calendar, DateEntry

def configure_dateentry_style():
    """Configure le style du DateEntry et du calendrier pour correspondre à l'apparence de l'application."""
    style = ttk.Style()
    style.theme_use('default')

    # Style du DateEntry
    style.configure("TDateEntry", fieldbackground="#e0e0e0", foreground="black", font=("Helvetica", 10))
    style.map("TDateEntry", fieldbackground=[("readonly", "#e0e0e0")])

    # Style du calendrier
    style.configure("TCalendar", background="#4a90e2", foreground="white", font=("Helvetica", 10), borderwidth=0)
    style.configure("TCalendar.Month", background="#4a90e2", foreground="white", font=("Helvetica", 10), padding=5)
    style.configure("TCalendar.Day", background="white", foreground="black", font=("Helvetica", 10), padding=2)
    style.map("TCalendar.Day", background=[("selected", "#4a90e2")], foreground=[("selected", "white")])

def configure_dateentry_style(date_entry_widget):
    """Configure le style du DateEntry et son calendrier."""
    # Configurer les couleurs du DateEntry
    date_entry_widget.config(
        background="#4a90e2",  # Fond bleu clair pour correspondre au bouton "Enregistrer"
        foreground="white",    # Texte blanc
        headersbackground="#4a90e2",  # Fond bleu pour les en-têtes (jours de la semaine)
        headersforeground="white",    # Texte blanc pour les en-têtes
        selectbackground="#4a90e2",   # Fond bleu pour les dates sélectionnées
        selectforeground="white",     # Texte blanc pour les dates sélectionnées
        font=("Helvetica", 10)        # Police Helvetica
    )