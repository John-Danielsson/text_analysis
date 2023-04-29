from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from requests import get
from re import sub
from datetime import datetime
from os.path import basename
from docx import Document
import fitz


class FileParser:


    """Initializes the FileParser and calculates the text output
    based on the file extension"""
    def __init__(self, filepath: str):
        self.text = []
        self.filename = basename(filepath)
        if filepath.endswith(".epub"):
            self.extension = ".epub"
            self.text = self.parse_epub(filepath)
        elif filepath.startswith("http"):
            self.extension = "http"
            self.text = self.parse_online_html(filepath)
        elif filepath.endswith(".html"):
            self.extension = ".html"
            self.text = self.parse_local_html(filepath)
        elif filepath.endswith(".pdf"):
            self.extension = ".pdf"
            self.text = self.parse_pdf(filepath)
        elif filepath.endswith(".txt"):
            self.extension = ".txt"
            self.text = self.parse_txt(filepath)
        elif filepath.endswith(".docx") or filepath.endswith(".doc"):
            self.extension = ".doc"
            if filepath.endswith(".docx"):
                self.extension += "x"
            self.text = self.parse_docx_or_doc(filepath)


    """Returns the text representation of the given file."""
    def __str__(self):
        # def clean_text(text: str) -> str:
        #     return text.encode(
        #         encoding="utf-8",
        #         errors="ignore"
        #     ).decode(
        #         encoding="utf-8",
        #         errors="ignore"
        #     )
        # return "\n".join(clean_text(x) for x in self.text)
        return "\n".join(p for p in self.text)


    """Parses text from a website."""
    @staticmethod
    def parse_online_html(link: str) -> list:
        soup = BeautifulSoup(get(link).content, "html.parser")
        return [p.get_text() for p in soup.find_all("p")]


    """Parses text from a an HTML file"""
    @staticmethod
    def parse_local_html(filepath: str) -> list:
        with open(filepath, 'r') as f:
            html = f.read()
        bs4_html = BeautifulSoup(html, "html.parser")
        return [p.get_text() for p in bs4_html.find_all("p")]


    """Parses <p> tags from the given HTML."""
    @staticmethod
    def html_to_str(html) -> str:
        bs4_html = BeautifulSoup(html, "html.parser")
        return "\n".join(p.get_text() for p in bs4_html.find_all("p"))


    """Parses text from a .epub file."""
    def parse_epub(self, filepath: str) -> list:
        file = epub.read_epub(filepath)
        items = list(file.get_items_of_type(ITEM_DOCUMENT))
        return [self.html_to_str(item.get_content()) for item in items]


    """Parses text from a .pdf file."""
    @staticmethod
    def parse_pdf(filepath: str) -> list:
        pdf = fitz.open(filepath)
        return [page.get_text() for page in pdf]


    """Parses text from a .txt file."""
    @staticmethod
    def parse_txt(filepath: str) -> list:
        with open(file=filepath, mode="r", errors="ignore") as file:
            return file.read().split("\n")


    """Parses text from a .docx file."""
    @staticmethod
    def parse_docx_or_doc(filepath: str) -> list:
        document = Document(filepath)
        return [p.text for p in document.paragraphs]


    """Saves the file to a .txt file in the given filepath."""
    def to_txt(self, filepath: str) -> None:
        timestamp = sub("[ -:.]", "_", datetime.now().__str__())
        filepath = f"{filepath}/{self.filename}_{timestamp}.txt"
        with open(file=filepath, mode="w", encoding="utf-8", errors="ignore") as file:
            file.write(self.__str__())
