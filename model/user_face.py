from insightface.app.common import Face
from insightface.model_zoo.model_zoo import get_model
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class UserFace:
    def __init__(self):
        self.decoder = get_model('./insight_face_models/models/buffalo_l/det_10g.onnx')
        self.decoder.prepare(ctx_id=0, input_size=(640, 640))
        self.encoder = get_model('./insight_face_models/models/buffalo_l/w600k_r50.onnx')
        self.encoder.prepare(ctx_id=0)
    
    def detect_faces(self, image):
        face_boxes, kpss = self.decoder.detect(img=image)
        
        detected_faces = []
        for face_box, kps in zip(face_boxes, kpss):
            detected_face = Face(bbox=face_box[0:4], kps=kps)
            detected_faces.append(detected_face)

        self.encoder.get(img=image, face=detected_faces[0])
            
        return detected_faces[0]
    
    def estimate_cosine_similarity(self, embedding1, embedding2):
        a = np.matmul(embedding1.T, embedding2)
        b = np.sum(np.multiply(embedding1, embedding1))
        c = np.sum(np.multiply(embedding2, embedding2))
        return a / (np.sqrt(b) * np.sqrt(c))

    def make_image(self, image1_path: str, image2_path: str, scale: float = 0.8, new_height: int = 600) -> Image:
        image_scale = 0.5 * scale + 0.5

        # 画像を開く
        left_image = Image.open(image1_path).convert('RGBA')
        middle_image = Image.open('./data/heart.png').convert('RGBA')
        right_image = Image.open(image2_path).convert('RGBA')

        # 左右の画像の高さを指定の高さにリサイズ
        left_image = left_image.resize((int(left_image.width * new_height / left_image.height), new_height))
        middle_image = middle_image.resize((int(middle_image.width * int(new_height/3) / middle_image.height), int(new_height/3)))
        right_image = right_image.resize((int(right_image.width * new_height / right_image.height), new_height))

        # テキストを追加
        draw = ImageDraw.Draw(middle_image)
        # font_size = int(100 * image_scale)  # フォントサイズをimage_scaleに基づいて調整
        font = ImageFont.truetype('arial.ttf', 50)  # フォントとサイズを選択
        draw.text((55, 65), "{:.3f}".format(scale), fill='black', font=font)  # テキストの位置、内容、色、フォントを指定

        # 中央の画像をスケーリング
        width, height = middle_image.size
        middle_image = middle_image.resize((int(width*image_scale*2.5), int(height*image_scale*2.5)))

        # 新しい画像のサイズを計算
        new_width = max(left_image.width, middle_image.width, right_image.width) * 3
        new_height = max(left_image.height, middle_image.height, right_image.height)

        # 新しい画像を作成
        new_image = Image.new('RGBA', (new_width, new_height))

        # 画像を新しい画像に貼り付け
        new_image.paste(left_image, ((new_width // 3 - left_image.width) // 2, (new_height - left_image.height) // 2))
        new_image.paste(middle_image, ((new_width // 3 - middle_image.width) // 2 + new_width // 3, (new_height - middle_image.height) // 2), middle_image)
        new_image.paste(right_image, ((new_width // 3 - right_image.width) // 2 + new_width * 2 // 3, (new_height - right_image.height) // 2))

        return new_image