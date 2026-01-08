class Session:
    def __init__(self, date: str, time: str, values: dict):
        self.date = date      # YYYY-MM-DD
        self.time = time      # HH:MM
        self.values = values

    def to_dict(self):
        return {
            "date": self.date,
            "time": self.time,
            "values": self.values,
        }
