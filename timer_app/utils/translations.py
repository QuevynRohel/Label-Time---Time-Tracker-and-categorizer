# utils/translations.py
import os
import locale

# Définissez les traductions disponibles
translations = {
    "en": {
        "TIME TRACKER": "TIME TRACKER",
        "Statistiques": "Statistics",
        "Ajouter une entrée": "Add an Entry",
        "Démarrer une session": "Start a Session",
        "Options": "Options",
        "Langues": "Languages",
        "Retour": "Back",
        "Temps de {time} sur '{category}' enregistré avec succès !": "Time of {time} on '{category}' successfully saved!",
    },
    "fr": {
        "TIME TRACKER": "LE TRAQUEUR DE TEMPS",
        "Statistiques": "Statistiques",
        "Ajouter une entrée": "Ajouter une entrée",
        "Démarrer une session": "Démarrer une session",
        "Options": "Options",
        "Langues": "Langues",
        "Retour": "Retour",
        "Temps de {time} sur '{category}' enregistré avec succès !": "Temps de {time} sur '{category}' enregistré avec succès !",
    }
}

# Détection automatique de la langue du système
system_language = locale.getdefaultlocale()[0][:2]
lang = os.getenv("APP_LANG", system_language if system_language in translations else "en")

def _(text):
    """Fonction de traduction."""
    return translations.get(lang, {}).get(text, text)

def set_language(language):
    """Modifie la langue globalement."""
    global lang
    lang = language

def get_available_languages():
    """Retourne les langues disponibles dans le fichier de traduction."""
    return list(translations.keys())