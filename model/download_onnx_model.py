from insightface.app import FaceAnalysis

def download_onnx_model():
    FaceAnalysis(name='buffalo_l', root='./insight_face_models/')