from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import chromadb
import os
import glob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
DATA_DIR = "src/phase_1_ingestion/data"
EMBEDDING_MODEL = "models/gemini-embedding-001"
COLLECTION_NAME = "hdfc_mutual_funds"

def get_markdown_files(directory):
    return glob.glob(os.path.join(directory, "*.md"))

def process_and_embed():
    # 1. Initialize Embedding Model (Google Gemini)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return

    print(f"Initializing Gemini Embedding Model: {EMBEDDING_MODEL}...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=api_key
    )

    # 2. Get all Markdown files
    md_files = get_markdown_files(DATA_DIR)
    if not md_files:
        print("No markdown files found to process.")
        return

    all_docs = []
    
    # 3. Setup Splitters
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)

    for file_path in md_files:
        print(f"Processing {file_path}...")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split by Markdown Headers first
            header_splits = markdown_splitter.split_text(content)
            
            # Further split into smaller chunks if needed
            final_splits = text_splitter.split_documents(header_splits)
            
            # Add metadata from the file name
            filename = os.path.basename(file_path)
            for doc in final_splits:
                doc.metadata["source_file"] = filename
                
            all_docs.extend(final_splits)
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    if not all_docs:
        print("No documents generated after splitting.")
        return

    # 4. Initialize Chroma Cloud Client
    print("Connecting to Chroma Cloud...")
    try:
        # Chroma Cloud environment variables
        chroma_api_key = os.getenv("CHROMA_API_KEY")
        tenant = os.getenv("CHROMA_TENANT")
        database = os.getenv("CHROMA_DATABASE")

        # Use CloudClient for Chroma Cloud connection
        client = chromadb.CloudClient(
            tenant=tenant,
            database=database,
            api_key=chroma_api_key
        )

        # 5. Push to Cloud Collection with Rate Limiting
        print(f"Pushing {len(all_docs)} chunks to cloud collection: {COLLECTION_NAME}...")
        
        # Batching to respect Gemini Free Tier limits (100 RPM)
        batch_size = 90  # Staying slightly under the 100 limit
        
        # Create initial vector store with first batch
        first_batch = all_docs[:batch_size]
        vector_db = Chroma.from_documents(
            documents=first_batch,
            embedding=embeddings,
            client=client,
            collection_name=COLLECTION_NAME
        )
        
        # Process remaining batches
        import time
        for i in range(batch_size, len(all_docs), batch_size):
            print(f"Waiting 60s to avoid rate limits... ({i}/{len(all_docs)} processed)")
            time.sleep(60)
            
            next_batch = all_docs[i : i + batch_size]
            vector_db.add_documents(documents=next_batch)
            
        print("Cloud database successfully updated.")
        
    except Exception as e:
        print(f"Error connecting to Chroma Cloud: {e}")
        print("Ensure CHROMA_API_KEY, CHROMA_TENANT, and CHROMA_DATABASE are set.")

if __name__ == "__main__":
    process_and_embed()
