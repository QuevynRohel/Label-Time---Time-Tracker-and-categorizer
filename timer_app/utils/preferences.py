import json
import os
from utils.constants import PREFERENCES_FILE

def load_preferences():
    """Charge les préférences de langue depuis preferences.json."""
    if os.path.exists(PREFERENCES_FILE):
        with open(PREFERENCES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    # Si le fichier n'existe pas, retourne les préférences par défaut
    return {"language": "en"}

def save_preferences(preferences):
    """Enregistre les préférences de langue dans preferences.json."""
    with open(PREFERENCES_FILE, "w", encoding="utf-8") as file:
        json.dump(preferences, file)