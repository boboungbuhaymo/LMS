import re
import spacy
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import requests

nlp = spacy.load("en_core_web_sm")

def read_pdf(file_path):
    """Extract text from PDF files"""
    text = ""
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def read_txt(file_path):
    """Read plain text files"""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def scrape_webpage(url):
    """Extract text content from a webpage"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def extract_questions(text):
    """Identify questions in text using regex patterns"""
    question_pattern = r"(?:^|\n)\s*\d+\.\s*(.+?\?)"
    return re.findall(question_pattern, text)

def calculate_similarity(text1, text2):
    """Calculate semantic similarity between two texts using spaCy"""
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    return doc1.similarity(doc2)