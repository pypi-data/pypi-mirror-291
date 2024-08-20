from bs4 import BeautifulSoup, CData, NavigableString
from ._base import RawDoc

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


class HTMLoader(RawDoc):
    def extract_text(self):
        with self.get_content() as file:
            soup = BeautifulSoup(file.decode(), "lxml")
            for paragraph in soup.get_text(
                separator="\n", strip=True, types=(NavigableString, CData)
            ):
                yield paragraph

    def extract_image(self):
        with self.get_content() as file:
            soup = BeautifulSoup(file.decode(), "lxml")
            for image in soup.find_all("img"):
                yield image.get("src", "")
