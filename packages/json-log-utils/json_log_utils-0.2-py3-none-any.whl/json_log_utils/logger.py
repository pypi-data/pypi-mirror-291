import os
import json
import csv
import uuid
from datetime import datetime


class Logger:
    def __init__(self, log_dir="logs", pipeline_id=None):
        self.log_dir = log_dir
        self.pipeline_id = pipeline_id if pipeline_id else str(uuid.uuid4())
        self.session_id = str(uuid.uuid4())
        self.session_dir = os.path.join(log_dir, self.pipeline_id, self.session_id)
        os.makedirs(self.session_dir, exist_ok=True)

    def log(self, data: dict, file_format="json"):
        """Log data in the specified file format (json, csv, etc.)."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"log_{timestamp}.{file_format}"
        log_path = os.path.join(self.session_dir, log_filename)

        if file_format == "json":
            self._log_json(data, log_path)
        elif file_format == "csv":
            self._log_csv(data, log_path)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")

    def _log_json(self, data, log_path):
        """Save data as a JSON file."""
        with open(log_path, "w") as f:
            json.dump(data, f, indent=4)

    def _log_csv(self, data, log_path):
        """Save data as a CSV file."""
        if not isinstance(data, dict):
            raise ValueError("Data for CSV logging must be a dictionary.")

        with open(log_path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data.keys())  
            writer.writerow(data.values()) 



