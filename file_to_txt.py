from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from requests import get
from PyPDF2 import PdfFileReader
from os.path import basename, join
from re import sub
from docx import Document

class FileToTXT:

    """Initializes the FileParser and calculates the text output
    based on the file extension"""
    def __init__(self, filepath: str):
        self.text = []
        if filepath.endswith('.txt'):
            self.text = self.parse_txt(filepath)
            self.filename = basename(filepath)[:-4]
        elif filepath.endswith('.epub'):
            self.text = self.parse_epub(filepath)
            self.filename = basename(filepath)[:-5]
        elif filepath.startswith("http"):
            self.text = self.parse_online_html(filepath)
            cleaned_url = sub(r'https?://', '', filepath)
            self.filename = sub(r'[^\w]', '_', cleaned_url)
        elif filepath.endswith('.html'):
            self.text = self.parse_local_html(filepath)
            self.filename = basename(filepath)[:-5]
        elif filepath.endswith('.pdf'):
            self.text = self.parse_pdf(filepath)
            self.filename = basename(filepath)[:-4]
        elif filepath.endswith('.docx'):
            self.text = self.parse_docx(filepath)
            self.filename = basename(filepath)[:-5]

    """Returns the text representation of the given file."""
    def __str__(self) -> str:
        def clean_text(text: str) -> str:
            encoded = text.encode(encoding="utf-8", errors="ignore")
            text = encoded.decode(encoding="utf-8", errors="ignore")
            text = text.replace('\n', ' ')
            text = sub(r'\s+', ' ', text)
            text = sub(r'[^a-zA-Z0-9\s]', '', text)
            return text.lower()
        return "\n".join(clean_text(x) for x in self.text)

    """Returns the text content of the given file."""
    def text(self) -> str:
        return self.__str__()

    """Parses text from a website. The URL must go to an HTML site."""
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
    @staticmethod
    def html_to_str(html) -> str:
        bs4_html = BeautifulSoup(html, "html.parser")
        return "\n".join(p.get_text() for p in bs4_html.find_all("p"))

    """Parses text from a .txt file."""
    def parse_txt(self, filepath: str) -> list:
        with open(file=filepath, mode="r") as file:
            return [file.read()]

    """Parses text from a .epub file."""
    def parse_epub(self, filepath: str) -> list:
        file = epub.read_epub(filepath)
        items = list(file.get_items_of_type(ITEM_DOCUMENT))
        return [self.html_to_str(item.get_content()) for item in items]

    """Parses text from a .pdf file."""
    def parse_pdf(self, filepath: str) -> list:
        with open(filepath, 'rb') as file:
            pdf = PdfFileReader(file)
            n_pages = pdf.getNumPages()
            result = []
            for i in range(n_pages):
                result.append(pdf.getPage(i).extractText())
            return result

    """Parses text from a .docx file."""
    def parse_docx(self, filepath: str) -> list:
        document = Document(filepath)
        return [p.text for p in document.paragraphs]

    """Saves the text to a .txt file in the given directory."""
    def save_to_directory(self, destination_directory: str) -> None:
        filepath = f"{join(destination_directory, self.filename)}.txt"
        with open(file=filepath, mode="w", encoding="utf-8", errors="ignore") as file:
            file.write(self.__str__())
