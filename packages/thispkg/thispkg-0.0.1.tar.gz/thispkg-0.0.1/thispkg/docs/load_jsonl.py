from ._base import RawDoc


class JsonLoader(RawDoc):
    def extract_text(self):
        with self.get_content() as file:
            yield file.decode()

    def extract_image(self):
        yield ""
