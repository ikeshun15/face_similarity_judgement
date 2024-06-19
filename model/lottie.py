import json

from .settting import Setting


class JsonHandler:
    @staticmethod
    def load(filepath) -> str:
        with open(filepath, "r") as f:
            return json.load(f)


PROCESSING_LOTTIE = JsonHandler.load(filepath=Setting.PROCESSING_LOTTIE_PATH)
