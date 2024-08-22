from .data_loader import DataLoader
from .utils import cosine_similarity, scan_document
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
import numpy as np

def load_embeddings():
    return HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def process_chunks(chunks, query, k=5):
    embeddings = load_embeddings()
    vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)

    query_embedding = embeddings.embed_query(query)
    document_embeddings = vectorstore.index.reconstruct_n(0, vectorstore.index.ntotal)
    
    similarities = [cosine_similarity(query_embedding, doc_embedding) for doc_embedding in document_embeddings]
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    
    results = [(vectorstore.docstore.search(vectorstore.index_to_docstore_id[i]), similarities[i]) for i in top_k_indices]
    
    return results

def search_document(filepath_or_url, query, chunk_size=1024, chunk_overlap=80, k=5):
    data_loader = DataLoader(filepath_or_url)
    chunks = data_loader.process_document(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return process_chunks(chunks, query, k)

def scan_and_search(image, query, chunk_size=1024, chunk_overlap=80, k=5):
    scanned_text = scan_document(image)
    document = LangChainDocument(page_content=scanned_text, metadata={"source": "Scanned Document"})
    chunks = DataLoader("").chunk_document([document], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return process_chunks(chunks, query, k)