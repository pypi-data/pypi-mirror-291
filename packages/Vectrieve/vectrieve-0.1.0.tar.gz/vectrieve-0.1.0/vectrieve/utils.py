import numpy as np
from PIL import Image
import pytesseract
from langchain.schema import Document as LangChainDocument

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def scan_document(image):
    text = pytesseract.image_to_string(image)
    return text