class Session:
    def __init__(self, date: str, values: dict, activity_name: str | None = None):
        self.date = date
        if activity_name:
            from models.activities import ACTIVITIES
            allowed = ACTIVITIES.get(activity_name, [])
            self.values = {k: values.get(k) for k in allowed}
        else:
            self.values = values

    def to_dict(self):
        return {
            "date": self.date,
            "values": self.values
        }
