from setuptools import setup, find_packages

setup(
    name="Vectrieve",
    version="0.1.0",
    author="Ahsan Ali",
    author_email="ahsanai440@gmail.com",
    description="Enhanced Document Semantic Search with Cosine Similarity and Document Scanning",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/enhanced-document-search",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.10.0",
        "langchain-text-splitters>=0.0.2",
        "langchain-community>=0.0.2",
        "numpy>=1.19.2",
        "pandas>=1.1.3",
        "docx2txt>=0.8",
        "Pillow>=8.0.1",
        "pytesseract>=0.3.8",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)