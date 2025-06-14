import logging
from datetime import datetime

from django.conf import settings
from pymongo import MongoClient


class MongoHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]
        self.collection = self.db["logs"]

    def emit(self, record):
        try:
            log_entry = {
                "level": record.levelname,
                "message": record.getMessage(),
                "timestamp": datetime.now(),
                "logger": record.name,
                "module": record.module,
                "funcName": record.funcName,
                "line": record.lineno,
                "path": record.pathname,
            }
            self.collection.insert_one(log_entry)
        except Exception:
            self.handleError(record)
