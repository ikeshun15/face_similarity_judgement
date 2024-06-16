from insightface.app import FaceAnalysis


def download_model(model_name: str = "buffalo_l"):
    FaceAnalysis(name=model_name, root="./insight_face_models/")
