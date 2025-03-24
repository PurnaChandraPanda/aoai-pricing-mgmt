import csv
import os

class CSVLogger:
    def __init__(self):
        # Initialize the file name as universal one in this logger
        self._filename = 'aoai_requests.csv'

        # Check if the file already exists
        file_exists = os.path.isfile(self._filename)

        # Create the CSV file and write the header if it doesn't exist
        if not file_exists:
            with open(self._filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['datetime', 'deployment', 'model', 'operation', 'prompt_tokens', 'completion_tokens','total_tokens'])

    def log(self, datetime, deployment, model, operation, prompt_tokens=None, completion_tokens=None, total_tokens=None):
        # Append a new row to the CSV file
        with open(self._filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime, deployment, model, operation, prompt_tokens, completion_tokens, total_tokens])