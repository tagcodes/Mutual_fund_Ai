def check_advisory(user_question):
    """
    Checks if the user question contains advisory keywords.
    Returns a refusal response if advisory is detected, otherwise None.
    """
    advisory_keywords = ["should i", "which is better", "best fund", "recommend", "advice", "compare"]
    
    if any(kw in user_question.lower() for kw in advisory_keywords):
        return {
            "answer": "I am a facts-only assistant and cannot provide investment advice or recommendations. Please refer to official SEBI or AMFI guidelines for advisory support.",
            "sources": ["https://www.amfiindia.com/investor-corner"],
            "last_updated": "N/A"
        }
    return None
