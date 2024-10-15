import csv
from datetime import datetime
from utils.constants import CSV_FILE_PATH, CSV_HEADERS

class CSVController:
    def __init__(self):
        self.initialize_csv()

    def initialize_csv(self):
        try:
            with open(CSV_FILE_PATH, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                if not list(reader):  # Fichier vide
                    self.write_headers()
        except (FileNotFoundError, UnicodeDecodeError):
            # Tentative avec un autre encodage en cas d'erreur
            try:
                with open(CSV_FILE_PATH, "r", encoding="ISO-8859-1") as file:
                    reader = csv.reader(file)
                    if not list(reader):
                        self.write_headers()
            except FileNotFoundError:
                self.write_headers()

    def write_headers(self):
        with open(CSV_FILE_PATH, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)

    def save_entry(self, category, description, elapsed_seconds):
        """Enregistre une entrée dans le fichier CSV avec la date actuelle, catégorie, description et durée."""
        with open(CSV_FILE_PATH, "a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                elapsed_seconds, 
                category, 
                description
            ])

    def get_categories(self):
        """Récupère l'ensemble des catégories du fichier CSV."""
        categories = set()
        try:
            with open(CSV_FILE_PATH, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    categories.add(row["Catégorie"])
        except FileNotFoundError:
            pass
        return categories