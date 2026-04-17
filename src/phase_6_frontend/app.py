import streamlit as st
import sys
import os
from datetime import datetime

# Add the project root to sys.path to allow imports from other phases
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.phase_3_retrieval.engine import FactualFAQAssistant

# --- Page Configuration ---
st.set_page_config(
    page_title="HDFC Mutual Fund FAQ Assistant",
    page_icon="📈",
    layout="wide"
)

# --- Styling ---
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .disclaimer {
        color: #ff4b4b;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border: 1px solid #ff4b4b;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .source-link {
        font-size: 0.8em;
        color: #1f77b4;
    }
    .footer {
        font-size: 0.8em;
        color: #666;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("Assistant Info")
    st.markdown("### Facts-only. No investment advice.")
    st.info("""
    This assistant provides factual information about the following HDFC Mutual Fund schemes:
    - HDFC Mid Cap Fund
    - HDFC Equity Fund
    - HDFC Focused Fund
    - HDFC ELSS Tax Saver Fund
    - HDFC Large Cap Fund
    """)
    
    st.divider()
    st.markdown("### Official Sources")
    st.markdown("- [Groww Mutual Funds](https://groww.in/mutual-funds)")
    st.markdown("- [SEBI](https://www.sebi.gov.in/)")
    st.markdown("- [AMFI](https://www.amfiindia.com/)")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Main Logic ---
st.title("📈 HDFC Mutual Fund FAQ Assistant")
st.markdown('<div class="disclaimer">⚠️ Disclaimer: This assistant provides facts-only information. It does NOT provide investment advice or recommendations.</div>', unsafe_allow_html=True)

# Initialize Assistant
@st.cache_resource
def load_assistant():
    try:
        return FactualFAQAssistant()
    except Exception as e:
        st.error(f"Error initializing assistant: {e}")
        return None

assistant = load_assistant()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Example Questions ---
st.markdown("### Example Questions")
col1, col2, col3 = st.columns(3)
example_q = ""

if col1.button("Exit load for HDFC Mid Cap?"):
    example_q = "What is the exit load for HDFC Mid Cap Fund?"
if col2.button("Minimum SIP for HDFC Equity?"):
    example_q = "What is the minimum SIP amount for HDFC Equity Fund?"
if col3.button("Riskometer for HDFC Focused?"):
    example_q = "Tell me about the riskometer classification for HDFC Focused Fund."

# Handle Input
prompt = st.chat_input("Ask a factual question about HDFC Mutual Funds...")
if example_q:
    prompt = example_q

if prompt:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    if assistant:
        with st.chat_message("assistant"):
            with st.spinner("Retrieving facts..."):
                result = assistant.query(prompt)
                
                # Format Response
                response_text = result["answer"]
                sources = result["sources"]
                last_updated = result["last_updated"]
                
                # Render Answer
                st.markdown(response_text)
                
                # Render Footer (Sources & Date)
                if sources and sources[0] != "N/A":
                    st.markdown(f"**Source:** [{sources[0]}]({sources[0]})", unsafe_allow_html=True)
                    st.markdown(f'<div class="footer">Last updated from sources: {last_updated}</div>', unsafe_allow_html=True)
                
                # Add assistant message to chat
                st.session_state.messages.append({"role": "assistant", "content": response_text})
    else:
        st.error("Assistant engine failed to load. Please check your configuration.")
