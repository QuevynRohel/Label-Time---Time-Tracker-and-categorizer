
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
            try:
                with open(CSV_FILE_PATH, "r", encoding="ISO-8859-1") as file:
                    reader = csv.reader(file)
                    if not list(reader):
                        self.write_headers()
            except FileNotFoundError:
                print(CSV_FILE_PATH + " NOT FOUND" )
                self.write_headers()

    def write_headers(self):
        with open(CSV_FILE_PATH, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)

    def save_entry(self, category, description, elapsed_seconds, date=None):
        """Enregistre une entrée dans le fichier CSV avec la date actuelle, catégorie, description et durée."""

        final_date = date if date is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CSV_FILE_PATH, "a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                final_date, 
                elapsed_seconds, 
                category, 
                description
            ])

    def get_categories(self):
        """Récupère l'ensemble des catégories du fichier CSV, triées de la plus récemment utilisée à la plus ancienne."""
        categories_with_dates = {}
        
        try:
            with open(CSV_FILE_PATH, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    category = row["Catégorie"]
                    # Parse the date
                    entry_date = datetime.strptime(row["Date"], "%Y-%m-%d %H:%M:%S")
                    
                    # Mettez à jour la date si la catégorie a une entrée plus récente
                    if category not in categories_with_dates or entry_date > categories_with_dates[category]:
                        categories_with_dates[category] = entry_date

        except FileNotFoundError:
            pass

        # Trier les catégories par date, de la plus récente à la plus ancienne
        sorted_categories = sorted(categories_with_dates, key=categories_with_dates.get, reverse=True)

        return sorted_categories