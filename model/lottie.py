import json


class JsonHandler:
    @staticmethod
    def load(filepath) -> str:
        with open(filepath, "r") as f:
            return json.load(f)


PROCESSING_LOTTIE_PATH = "./data/processing.json"
PROCESSING_LOTTIE = JsonHandler.load(filepath=PROCESSING_LOTTIE_PATH)
