import os
from dotenv import load_dotenv
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

def verify_gemini():
    print("--- Verifying Gemini API ---")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or "your_" in api_key:
        print("❌ Error: GEMINI_API_KEY is missing or still a placeholder.")
        return False
    
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        # Try a small embedding
        embeddings.embed_query("Hello world")
        print("✅ Gemini API is working correctly.")
        return True
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return False

def verify_chroma():
    print("\n--- Verifying Chroma Cloud ---")
    api_key = os.getenv("CHROMA_API_KEY")
    tenant = os.getenv("CHROMA_TENANT")
    database = os.getenv("CHROMA_DATABASE")
    
    if not api_key or "your_" in api_key:
        print("❌ Error: CHROMA_API_KEY is missing or still a placeholder.")
        return False
    
    try:
        client = chromadb.CloudClient(
            tenant=tenant,
            database=database,
            api_key=api_key
        )
        # Check heartbeat
        client.heartbeat()
        print(f"✅ Chroma Cloud is reachable (Tenant: {tenant}, DB: {database}).")
        return True
    except Exception as e:
        print(f"❌ Chroma Cloud Error: {e}")
        return False

if __name__ == "__main__":
    gemini_ok = verify_gemini()
    chroma_ok = verify_chroma()
    
    if gemini_ok and chroma_ok:
        print("\n🚀 All systems go! You are ready to run the ingestion pipeline.")
    else:
        print("\n⚠️ Please fix the issues above before proceeding.")
