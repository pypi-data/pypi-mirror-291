# 🚀 Enhanced Document Semantic Search

## Overview
The "Enhanced Document Semantic Search" package provides powerful tools for searching and analyzing documents using advanced natural language processing techniques. With this package, you can:

- **Search documents**: Quickly find relevant information within your documents by running semantic searches based on natural language queries.
- **Scan and search documents**: Easily extract text from images and PDFs, then perform semantic searches on the extracted content.
- **Utilize cutting-edge embeddings**: The package leverages the state-of-the-art Sentence Transformer model from Hugging Face to generate high-quality document and query embeddings.
- **Achieve high accuracy**: The package uses cosine similarity to rank document relevance, providing accurate and meaningful search results.

## Installation
You can install the "Enhanced Document Search" package using pip:

pip install enhanced-document-search

## Usage
Here's an example of how to use the package to search a document:

```python
from vectrieve.functions import search_document

# Search a document
results = search_document("path/to/document.pdf", "query")
for doc, score in results:
    print(f"Text: {doc.page_content}")
    print(f"Source: {doc.metadata.get('source', 'Unknown')}")
    print(f"Similarity: {score:.4f}")

And here's an example of how to use the package to scan and search a document:

from vectrieve.functions import scan_and_search
from PIL import Image

# Scan and search a document
image = Image.open("path/to/image.jpg")
results = scan_and_search(image, "query")
for doc, score in results:
    print(f"Text: {doc.page_content}")
    print(f"Source: {doc.metadata.get('source', 'Unknown')}")
    print(f"Similarity: {score:.4f}")

Features

Robust document loading: The package supports a variety of file formats, including PDF, DOCX, TXT, XLS, and XLSX.
Intelligent document chunking: The package automatically splits long documents into manageable chunks, ensuring efficient processing and search.
Highly accurate search: The use of cosine similarity and state-of-the-art embeddings provides accurate and relevant search results.
Seamless document scanning: The package can extract text from images using Tesseract OCR, allowing you to search scanned documents.

Contributing
We welcome contributions to the "Vectrieve" package. If you'd like to report a bug, request a feature, or contribute code, please visit the project's GitHub repository.
License
This project is licensed under the MIT License.

This README file provides a high-level overview of the "Vectrieve" package, including its key features, installation instructions, usage examples, and information on contributing to the project. Feel free to customize this template to fit your specific package and requirements.