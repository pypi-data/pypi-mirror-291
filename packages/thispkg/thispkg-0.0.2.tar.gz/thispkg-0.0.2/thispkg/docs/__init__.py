from typing import Literal, Type, Generator
from ._base import RawDoc
from .load_docx import DocxLoader
from .load_html import HTMLoader
from .load_jsonl import JsonLoader
from .load_markdown import MarkdownLoader
from .load_pdf import PdfLoader
from .load_pptx import PptxLoader
from .load_xlsx import ExcelLoader

Key = Literal[
    "docx", "doc", "html", "jsonl", "json", "md", "pdf", "pptx", "ppt", "xls", "xlsx"
]

MAPPING: dict[Key, Type[RawDoc]] = {
    "docx": DocxLoader,
    "doc": DocxLoader,
    "html": HTMLoader,
    "jsonl": JsonLoader,
    "json": JsonLoader,
    "md": MarkdownLoader,
    "pdf": PdfLoader,
    "pptx": PptxLoader,
    "ppt": PptxLoader,
    "xls": ExcelLoader,
    "xlsx": ExcelLoader,
}


def load_document(key: Key, source: str) -> Generator[str, None, None]:
    doc = MAPPING[key](src=source)
    for text in doc.extract_text():
        yield text
    for image in doc.extract_image():
        yield image


__all__ = ["load_document", "Key"]
