class Entry:
    def __init__(self, date, seconds, category, description):
        self.date = date
        self.seconds = seconds
        self.category = category
        self.description = description

    def to_csv_row(self):
        return [self.date, self.seconds, self.category, self.description]