from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
import streamlit as st
import numpy as np
import pytesseract
from PIL import Image

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def scan_document(image):
    text = pytesseract.image_to_string(image)
    return text

@st.cache_resource
def load_embeddings():
    return HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

embeddings = load_embeddings()

def process_chunks(chunks):
    if chunks:
        st.text_area("Document Preview", chunks[0].page_content[:1000] + "...", height=200)
        
        with st.spinner("🧠 Creating embeddings and FAISS index..."):
            vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
        
        st.success("Ready for questions!")
        
        query = st.text_input("🔎 Ask a question about the document")
        if query:
            k = st.slider("Number of results", min_value=1, max_value=10, value=5)
            
            with st.spinner("🕵️ Searching..."):
                query_embedding = embeddings.embed_query(query)
                document_embeddings = vectorstore.index.reconstruct_n(0, vectorstore.index.ntotal)
                
                similarities = [cosine_similarity(query_embedding, doc_embedding) for doc_embedding in document_embeddings]
                top_k_indices = np.argsort(similarities)[-k:][::-1]
                
                results = [(vectorstore.docstore.search(vectorstore.index_to_docstore_id[i]), similarities[i]) for i in top_k_indices]
            
            if results:
                for i, (doc, score) in enumerate(results, 1):
                    with st.expander(f"Match {i} - Similarity: {score:.4f}"):
                        st.write(f"**Text:** {doc.page_content}")
                        st.write(f"**Source:** {doc.metadata.get('source', 'Unknown')}")
            else:
                st.write("No matches found.")