import json
import os
import locale
from utils.constants import PREFERENCES_FILE, DEFAULT_LANGUAGE

def load_preferences(always_return_a_result=True):
    """Charge les préférences de langue depuis preferences.json."""
    if os.path.exists(PREFERENCES_FILE):
        with open(PREFERENCES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
        
    if not always_return_a_result:
        return {}
    # Si le fichier n'existe pas, retourne les préférences par défaut
    return {"language": DEFAULT_LANGUAGE}

def save_preferences(preferences):
    """Enregistre les préférences de langue dans preferences.json."""
    # Crée le répertoire si nécessaire
    os.makedirs(os.path.dirname(PREFERENCES_FILE), exist_ok=True)
    # Écrit les préférences dans le fichier JSON
    with open(PREFERENCES_FILE, "w", encoding="utf-8") as file:
        json.dump(preferences, file, ensure_ascii=False, indent=4)

