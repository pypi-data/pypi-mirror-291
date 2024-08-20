from ._base import RawDoc


class MarkdownLoader(RawDoc):
    def extract_text(self):
        with self.get_content() as file:
            for line in file.decode().splitlines():
                yield line

    def extract_image(self):
        yield ""
