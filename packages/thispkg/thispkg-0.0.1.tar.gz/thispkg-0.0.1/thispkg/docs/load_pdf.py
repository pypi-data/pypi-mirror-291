from pathlib import Path

from fitz import open as open_pdf  # type: ignore
from PyPDF2 import PdfReader

from ..base64 import base64
from ._base import RawDoc


class PdfLoader(RawDoc):
    def extract_text(self):  # type: ignore
        with self.get_file() as file:
            text_doc = PdfReader(Path(file))
            for page_number in range(len(text_doc.pages)):
                page = text_doc.pages[page_number]
                yield page.extract_text()

    def extract_image(self):
        with self.get_content() as file:
            img_doc = open_pdf(file)
            for page in img_doc:  # type: ignore
                for img in page.get_images():  # type: ignore
                    xref = img[0]  # type: ignore
                    base_image = img_doc.extract_image(xref)  # type: ignore
                    image_bytes = base_image["image"]  # type: ignore
                    assert isinstance(image_bytes, bytes)
                    yield base64.b64encode(image_bytes).decode()
