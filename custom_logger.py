import logging
from pathlib import Path


class CustomLogger:
    def __init__(self, filename) -> None:
        self.filename = Path.cwd() / 'output' / filename
        self.add_to_log("================================")

    def add_to_log(self, text):
        with open(self.filename, "a") as myfile:
            myfile.writelines(text + '\n')
