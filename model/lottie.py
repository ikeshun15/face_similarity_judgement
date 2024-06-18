import json


class JsonHandler:
    @staticmethod
    def load(filepath) -> str:
        with open(filepath, "r") as f:
            return json.load(f)


PROCCESSING_LOTTIE_PATH = "./data/processing.json"
PROCCESSING_LOTTIE = JsonHandler.load(filepath=PROCCESSING_LOTTIE_PATH)
