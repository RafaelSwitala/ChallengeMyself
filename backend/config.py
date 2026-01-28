import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_ENABLED = False     # True = an, False = aus
LOG_LEVEL = "DEBUG"        # DEBUG | INFO | WARNING | ERROR
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = "app.log"
