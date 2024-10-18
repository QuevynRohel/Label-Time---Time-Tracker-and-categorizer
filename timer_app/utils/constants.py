
import os
import sys

def get_data_path():
    """Retourne le chemin du dossier data en fonction du mode d'exécution."""
    if getattr(sys, 'frozen', False):  # Mode exécutable
        base_dir = os.path.dirname(sys.executable)
        data_path = os.path.join(base_dir, 'data')
        os.makedirs(data_path, exist_ok=True)  # Crée le dossier s'il n'existe pas
        return data_path
    
    else:  # Mode script
        return "data"

# Utilisation de get_data_path() pour définir les constantes de chemin
CSV_FILE_PATH = os.path.join(get_data_path(), "times.csv")
CSV_HEADERS = ["Date", "Temps en secondes", "Catégorie", "Description"]

PREFERENCES_FILE = os.path.join(get_data_path(), "preferences.json")
DEFAULT_LANGUAGE = "en"

# Noms des vues pour la navigation
VIEW_MAIN_MENU = "view_main_menu"
VIEW_STATS = "view_stats"
VIEW_ADD_ENTRY = "view_add_entry"
VIEW_SESSION = "view_session"
VIEW_OPTIONS = "view_options"