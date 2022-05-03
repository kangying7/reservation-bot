from pathlib import Path

class CustomLogger:
    def __init__(self, parent_folder_path, filename) -> None:
        # Create output folder if does not exist
        # output_folder = Path.cwd() / 'output'
        # Path(parent_folder_path).mkdir(parents=True, exist_ok=True)

        self.filename = Path(parent_folder_path) / filename
        # self.add_to_log("================================")

    def add_to_log(self, text):
        with open(self.filename, "a") as myfile:
            myfile.writelines(text + '\n')
