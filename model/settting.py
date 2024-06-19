import os
from dotenv import load_dotenv

load_dotenv()


class Setting:
    FONT_TYPE = os.environ["FONT_TYPE"]
    HEART_IMAGE_PATH = "./data/heart.png"

    PROCESSING_LOTTIE_PATH = "./data/processing.json"

    MODEL_NAME = "buffalo_l"
    ROOT_DIR_PATH = "./insight_face_models/"
    DETECTOR_PATH = ROOT_DIR_PATH + "models/buffalo_l/det_10g.onnx"
    ENCODER_PATH = ROOT_DIR_PATH + "models/buffalo_l/w600k_r50.onnx"