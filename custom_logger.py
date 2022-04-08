from pathlib import Path

class CustomLogger:
    def __init__(self, filename) -> None:
        # Create output folder if does not exist
        output_folder = Path.cwd() / 'output'
        Path(output_folder).mkdir(parents=True, exist_ok=True)

        self.filename = output_folder / filename
        # self.add_to_log("================================")

    def add_to_log(self, text):
        with open(self.filename, "a") as myfile:
            myfile.writelines(text + '\n')
