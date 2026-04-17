from engine import FactualFAQAssistant
import sys

def main():
    print("--- Mutual Fund FAQ Assistant (Phase 4.2 Test) ---")
    try:
        assistant = FactualFAQAssistant()
    except Exception as e:
        print(f"Error initializing assistant: {e}")
        print("Please ensure GEMINI_API_KEY is set and ChromaDB is populated.")
        return

    test_queries = [
        "What is the exit load for HDFC Mid Cap Fund?",
        "Minimum SIP amount for HDFC Equity Fund?",
        "Should I invest in HDFC Focused Fund?",
        "Which fund is better: HDFC Mid Cap or HDFC Large Cap?"
    ]

    for query in test_queries:
        print(f"\nQUERY: {query}")
        result = assistant.query(query)
        print(f"ANSWER: {result['answer']}")
        print(f"SOURCES: {', '.join(result['sources'])}")
        print(f"LAST UPDATED: {result['last_updated']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
