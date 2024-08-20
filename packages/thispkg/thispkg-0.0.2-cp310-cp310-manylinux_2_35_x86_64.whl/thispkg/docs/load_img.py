from PIL import Image
from ..base64 import base64
from ._base import RawDoc


class ImageLoader(RawDoc):
    def extract_text(self):
        yield ""

    def extract_image(self):
        with self.get_content() as file:
            image = Image.open(file)
            yield base64.b64encode(image.tobytes()).decode()
