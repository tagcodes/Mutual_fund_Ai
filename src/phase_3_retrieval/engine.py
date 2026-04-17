import os
from dotenv import load_dotenv
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import sys
import os
# Ensure project root is in path for relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.phase_4_compliance.guardrails import check_advisory

# Load environment variables
load_dotenv()

# Constants
EMBEDDING_MODEL = "models/gemini-embedding-001"
LLM_MODEL = "llama-3.3-70b-versatile"
COLLECTION_NAME = "hdfc_mutual_funds"

class FactualFAQAssistant:
    def __init__(self):
        # API Keys and Cloud Settings
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        chroma_api_key = os.getenv("CHROMA_API_KEY")
        tenant = os.getenv("CHROMA_TENANT")
        database = os.getenv("CHROMA_DATABASE")
        groq_api_key = os.getenv("GROQ_API_KEY")

        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment.")

        # 1. Initialize Embeddings (Google Gemini)
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=gemini_api_key
        )

        # 2. Initialize Chroma Cloud Client
        self.cloud_client = chromadb.CloudClient(
            tenant=tenant,
            database=database,
            api_key=chroma_api_key
        )
        
        self.vector_db = Chroma(
            client=self.cloud_client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings
        )

        # 2. Initialize LLM (Groq)
        self.llm = ChatGroq(
            model_name=LLM_MODEL,
            groq_api_key=groq_api_key,
            temperature=0  # Strict factuality
        )

        # 3. Setup Multi-Query Retriever
        self.retriever = MultiQueryRetriever.from_llm(
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 3}),
            llm=self.llm
        )

        # 4. Define Factual System Prompt
        template = """You are a factual Mutual Fund FAQ Assistant. Your role is to answer questions based strictly on the provided context.
        
        CONSTRAINTS:
        - Answer facts-only. Do not provide investment advice, opinions, or recommendations.
        - If the question asks "Should I invest", "Which is better", or for any recommendation, refuse politely.
        - Every response must be concise and limited to a MAXIMUM of 3 sentences.
        - Every response must include the source link found in the context metadata.
        - If the answer is not in the context, say: "I'm sorry, I don't have that information in the official documents for the 5 HDFC schemes in scope."

        CONTEXT:
        {context}

        QUESTION: {question}

        FACTUAL ANSWER:"""
        
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

        # 5. Create Retrieval Chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def query(self, user_question):
        # Initial check for advisory keywords from Phase 4 Compliance
        refusal = check_advisory(user_question)
        if refusal:
            return refusal

        result = self.qa_chain({"query": user_question})
        answer = result["result"]
        source_docs = result["source_documents"]
        
        # Extract unique source URLs and the latest update date from metadata
        sources = list(set([doc.metadata.get("source_url", "N/A") for doc in source_docs]))
        last_updated = max([doc.metadata.get("last_updated", "Unknown") for doc in source_docs]) if source_docs else "Unknown"

        return {
            "answer": answer,
            "sources": sources,
            "last_updated": last_updated
        }

if __name__ == "__main__":
    # Internal test
    try:
        assistant = FactualFAQAssistant()
        print("Assistant initialized successfully.")
    except Exception as e:
        print(f"Error: {e}")
