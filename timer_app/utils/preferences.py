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
    # Crée le répertoire si nécessaire
    os.makedirs(os.path.dirname(PREFERENCES_FILE), exist_ok=True)
    # Écrit les préférences dans le fichier JSON
    with open(PREFERENCES_FILE, "w", encoding="utf-8") as file:
        json.dump(preferences, file, ensure_ascii=False, indent=4)

# Initialisation des préférences pour garantir l'existence du fichier
def initialize_preferences():
    """Vérifie l'existence du fichier preferences.json et crée des valeurs par défaut si nécessaire."""
    if not os.path.exists(PREFERENCES_FILE):
        save_preferences({"language": "en"})
