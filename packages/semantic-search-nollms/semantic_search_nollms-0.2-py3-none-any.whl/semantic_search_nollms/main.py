from .utils import load_embeddings, process_chunks, cosine_similarity, scan_document
from .web_crawler import WebCrawler
from .data_loader import DataLoader
import streamlit as st
from langchain.schema import Document as LangChainDocument
import os

def main():
    st.title("🚀 Enhanced Document Semantic Search with Web Crawling")
    st.markdown("### With Cosine Similarity (No LLM) and Document Scanning")

    st.sidebar.header("Options")
    chunk_size = st.sidebar.slider("Chunk Size", 256, 2048, 1024)
    chunk_overlap = st.sidebar.slider("Chunk Overlap", 0, 200, 80)

    # tab1, tab2, tab3 = st.tabs(["📄 Document Upload", "📷 Document Scan", "🌐 Web Crawl"])
    tab1, tab3 = st.tabs(["📄 Document Upload", "🌐 Web Crawl"])

    with tab1:
        uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT, XLS, XLSX)", type=["pdf", "docx", "txt", "xls", "xlsx"])
        
        if uploaded_file is not None:
            with st.spinner("🔍 Processing document..."):
                temp_file_path = f"temp_{uploaded_file.name}"
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                data_loader = DataLoader(temp_file_path)
                chunks = data_loader.process_document(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                os.remove(temp_file_path)
            
            process_chunks(chunks)

    # with tab2:
    #     st.write("📸 Scan a document using your camera or upload an image")
    #     scanned_image = st.camera_input("Take a picture of your document")
        
    #     if scanned_image:
    #         image = Image.open(scanned_image)
    #         with st.spinner("🔍 Scanning document..."):
    #             scanned_text = scan_document(image)
            
    #         st.success("Document scanned successfully!")
    #         st.text_area("Scanned Text", scanned_text, height=200)
            
    #         document = LangChainDocument(page_content=scanned_text, metadata={"source": "Scanned Document"})
    #         chunks = DataLoader("").chunk_document([document], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            
    #         process_chunks(chunks)

    with tab3:
        url = st.text_input("Enter URL to crawl", "")
        
        if url:
            with st.spinner("🌐 Crawling the web..."):
                crawler = WebCrawler(url)
                try:
                    content = crawler.fetch_content()
                    st.success("Content fetched successfully!")
                    st.text_area("Crawled Content", content[:2000], height=200)

                    document = LangChainDocument(page_content=content, metadata={"source": url})
                    chunks = DataLoader("").chunk_document([document], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    process_chunks(chunks)
                except Exception as e:
                    st.error(f"Error: {e}")



if __name__ == "__main__":
    main()