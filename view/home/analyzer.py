from PIL import Image
import pillow_heif
from streamlit.runtime.uploaded_file_manager import UploadedFile

from model import SimilarityAnalyzer


def analyze_similarity(uploaded_image1: UploadedFile, uploaded_image2: UploadedFile) -> Image.Image:
    image_rgb_1 = _open_image_as_rgb(uploaded_image1)
    image_rgb_2 = _open_image_as_rgb(uploaded_image2)
    analyzer = SimilarityAnalyzer(image_rgb_1=image_rgb_1, image_rgb_2=image_rgb_2)
    return analyzer.analyze()


def _open_image_as_rgb(uploaded_image: UploadedFile) -> Image.Image:
    uploaded_image_name: str = uploaded_image.name
    file_extension = uploaded_image_name.split(".")[-1].lower()

    if file_extension == "heic":
        heif_file = pillow_heif.read_heif(uploaded_image)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
    else:
        image = Image.open(uploaded_image)

    return image.convert("RGB")
