from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from requests import get
from PyPDF2 import PdfFileReader
from re import sub
from datetime import datetime
from os.path import basename

# Use this class to convert a given file into a .txt file to
# be read by LangChain's TextLoader? YES


class FileParser:

    """Initializes the FileParser and calculates the text output
    based on the file extension"""
    def __init__(self, filepath: str):
        self.text = []
        self.filename = basename(filepath)
        if filepath.endswith('.epub'):
            self.text = self.parse_epub(filepath)
        elif filepath.startswith("http"):
            # if filepath.endswith('.pdf'):
            # else:
            self.text = self.parse_online_html(filepath)
        elif filepath.endswith('.html'):
            self.text = self.parse_local_html(filepath)
        elif filepath.endswith('.pdf'):
            self.text = self.parse_pdf(filepath)

    """Returns the text representation of the given file."""
    def __str__(self):
        def clean_text(text: str) -> str:
            encoded = text.encode(encoding="utf-8", errors="ignore")
            return encoded.decode(encoding="utf-8", errors="ignore")
        return "\n".join(clean_text(x) for x in self.text)

    """Parses text from a website."""
    def parse_online_html(self, link: str) -> list:
        soup = BeautifulSoup(get(link).content, "html.parser")
        return [p.get_text() for p in soup.find_all("p")]

    """Parses text from a an HTML file"""
    def parse_local_html(self, filepath: str) -> list:
        with open(filepath, 'r') as f:
            html = f.read()
        bs4_html = BeautifulSoup(html, "html.parser")
        return [p.get_text() for p in bs4_html.find_all("p")]

    """Parses <p> tags from the given HTML."""
    def html_to_str(self, html) -> str:
        bs4_html = BeautifulSoup(html, "html.parser")
        return "\n".join(p.get_text() for p in bs4_html.find_all("p"))

    """Parses text from a .epub file."""
    def parse_epub(self, filepath: str) -> list:
        file = epub.read_epub(filepath)
        items = list(file.get_items_of_type(ITEM_DOCUMENT))
        return [self.html_to_str(item.get_content()) for item in items]

    """Parses text from a .pdf file."""
    def parse_pdf(self, filepath: str) -> list:
        pages = PdfFileReader(open(filepath, 'rb')).pages
        return [page.extract_text() for page in pages]

    def to_txt(self, filepath: str) -> None:
        timestamp = sub("[ -:.]", "_", datetime.now().__str__())
        filepath = f"{filepath}/{self.filename}_{timestamp}.txt"
        with open(file=filepath, mode="w", encoding="utf-8", errors="ignore") as file:
            file.write(self.__str__())
