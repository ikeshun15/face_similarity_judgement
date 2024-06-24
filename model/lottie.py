import json


def load_json(filepath: str) -> str:
    with open(filepath, "r") as f:
        return json.load(f)


PROCESSING_LOTTIE_PATH = "./data/processing.json"
PROCESSING_LOTTIE = load_json(filepath=PROCESSING_LOTTIE_PATH)
