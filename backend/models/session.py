class Session:
    def __init__(self, date: str, time: str, values: dict | None = None):
        self.date = date
        self.time = time
        self.values = values or {}

    def to_dict(self):
        return {
            "date": self.date,
            "time": self.time,
            "values": self.values,
        }
