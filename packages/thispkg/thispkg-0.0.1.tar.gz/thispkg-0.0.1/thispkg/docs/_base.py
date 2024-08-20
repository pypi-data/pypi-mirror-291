from abc import ABC, abstractmethod
from io import BytesIO
from requests import get
from dataclasses import dataclass
from typing import Generator
from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from pathlib import Path


@dataclass
class RawDoc(ABC):
    src: str

    @abstractmethod
    def extract_text(self) -> Generator[str, None, None]:
        pass

    @abstractmethod
    def extract_image(self) -> Generator[str, None, None]:
        pass

    @contextmanager
    def get_content(self):
        if self.src.startswith("http"):
            response = get(self.src)
            yield BytesIO(response.content).getvalue()
        else:
            with open(self.src, "rb") as file:
                yield file.read()

    @contextmanager
    def get_file(self):
        if self.src.startswith("http"):
            response = get(self.src)
            with NamedTemporaryFile(delete=False) as file:
                file.write(response.content)
                yield Path(file.name).as_posix()
        else:
            yield Path(self.src).as_posix()
