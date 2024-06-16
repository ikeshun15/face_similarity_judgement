from model import UserFace
from view import HomeComponents
from PIL import Image
import numpy as np

class HomeController:
    def main():
        face = UserFace()

        HomeComponents.init()
        HomeComponents.page_header()
        
        uploaded_file1, uploaded_file2, submit_pressed = HomeComponents.upload_images()

        if submit_pressed:
            if uploaded_file1 is not None and uploaded_file2 is not None:
                image1 = Image.open(uploaded_file1).convert('RGB')
                image2 = Image.open(uploaded_file2).convert('RGB')
                
                image1 = np.array(image1)
                image2 = np.array(image2)
                
                face1 = face.detect_faces(image1)
                face2 = face.detect_faces(image2)
                
                if face1 and face2:
                    similarity = face.estimate_cosine_similarity(face1.embedding, face2.embedding)
                    
                    combined_image = face.make_image(uploaded_file1, uploaded_file2, scale=similarity)
                    HomeComponents.display_combined_image(combined_image)
                else:
                    HomeComponents.display_error("画像から顔を検出できません")
            else:
                HomeComponents.display_error("二つの画像をアップロードしてください")
