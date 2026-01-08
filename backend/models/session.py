class Session:
    def __init__(self, date: str, values: dict):
        self.date = date
        self.values = values  # flexibel: km, minuten, zigaretten, etc.

    def to_dict(self):
        return {
            "date": self.date,
            "values": self.values
        }
