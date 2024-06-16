from insightface.app import FaceAnalysis

class ModelManager:
    ONNX = FaceAnalysis(name='buffalo_l', root='./insight_face_models/')