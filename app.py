import streamlit as st
import numpy as np
import faiss
import pickle
import re
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# -------------------------
# Configuration
# -------------------------
COLLEGE_NAME = "Siliguri Institute of Technology"
CONTACT_INFO = "+91‑9876543210 | info@sittech.edu.in"
WEBSITE = "sittech.ac.in"

# Preload models and resources (using cache)
@st.cache_resource(show_spinner=False)
def load_resources():
    """Load all heavy resources once and cache them"""
    resources = {}
    
    # Load knowledge base
    try:
        resources['index'] = faiss.read_index("faiss_store/index.faiss")
        with open("faiss_store/data.pkl", "rb") as f:
            resources['data'] = pickle.load(f)
    except Exception as e:
        st.error(f"Knowledge base error: {str(e)}")
        resources['index'] = None
        resources['data'] = None
    
    # Load embedding model
    try:
        resources['embedder'] = SentenceTransformer("all-MiniLM-L6-v2")
    except:
        resources['embedder'] = None
    
    # Configure Gemini
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        resources['gemini_model'] = genai.GenerativeModel("gemini-1.5-flash")
    except:
        resources['gemini_model'] = None
    
    return resources

# -------------------------
# Helper Functions
# -------------------------
def normalize_text(text):
    """Fast text normalization"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    # Quick synonym replacements
    text = re.sub(r'\b(hi|hello|hey|hlw|hii|greetings?)\b', 'greeting', text)
    text = re.sub(r'\b(courses?|programs?|degrees?)\b', 'programs', text)
    text = re.sub(r'\b(admission|apply|application)\b', 'admission', text)
    text = re.sub(r'\b(hostel|dorm|stay)\b', 'hostel', text)
    return re.sub(r'\s+', ' ', text)

def get_knowledge_response(query, resources):
    """Fast response from knowledge base"""
    if not resources['data']: 
        return None
    
    norm = normalize_text(query)
    
    # Quick greeting check
    if "greeting" in norm:
        return "Hi! How can I help you today?"
    
    # Vector search
    if resources['embedder'] and resources['index']:
        try:
            vec = resources['embedder'].encode([norm])
            D, I = resources['index'].search(vec.astype("float32"), k=1)
            if D[0][0] < 0.7:  # Good match threshold
                return resources['data']['answers'][I[0][0]]
        except:
            pass
    return None

def gemini_response(query, model):
    """Optimized Gemini fallback"""
    if not model:
        return f"Please contact us: {CONTACT_INFO}"
    
    try:
        prompt = (
            f"Answer briefly as {COLLEGE_NAME} assistant: {query} "
            f"Contact: {CONTACT_INFO} | Website: {WEBSITE}"
        )
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=150,  # Shorter responses
                temperature=0.3
            )
        )
        return response.text.strip()[:300]  # Limit response length
    except:
        return f"Please contact: {CONTACT_INFO}"

# -------------------------
# Streamlit UI
# -------------------------
def main():
    # Load all heavy resources (cached)
    resources = load_resources()
    
    # Page setup
    st.set_page_config(
        page_title=f"{COLLEGE_NAME} Assistant",
        page_icon="🏫",
        layout="centered"
    )
    
    # Apply theme
    st.markdown("""
    <style>
    :root {
        --primary: #2563eb;
        --background: #0f172a;
        --surface: #1e293b;
        --text: #e2e8f0;
    }
    body, .stApp {
        background-color: var(--background) !important;
        color: var(--text) !important;
        font-family: Arial, sans-serif;
    }
    .stChatMessage {
        max-width: 85%;
    }
    .stChatMessage.user .message-content {
        background-color: var(--primary);
        border-radius: 18px;
        padding: 12px 16px;
        color: white;
    }
    .stChatMessage.assistant .message-content {
        background-color: var(--surface);
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 12px 16px;
    }
    .token-counter {
        position: fixed;
        top: 70px;
        right: 20px;
        background: var(--surface);
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": (
                f"Hi! I'm the {COLLEGE_NAME} assistant. "
                "Ask me about:\n- Courses\n- Admission\n"
                "- Hostel\n- Placements\n- Contact"
            )
        }]
        st.session_state.token_count = 0
    
    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"]=="user" else "🏫"):
            st.markdown(f'<div class="message-content">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Token counter
    st.markdown(f'<div class="token-counter">Tokens used: {st.session_state.token_count}</div>', unsafe_allow_html=True)
    
    # Handle input
    user_input = st.chat_input("Ask about our college...")
    if user_input:
        # Add user message immediately for responsiveness
        with st.chat_message("user", avatar="🧑"):
            st.markdown(f'<div class="message-content">{user_input}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get response
        with st.spinner("Thinking..."):
            # First try knowledge base
            kb_response = get_knowledge_response(user_input, resources)
            
            if kb_response:
                response = kb_response
            else:
                # Fallback to Gemini
                response = gemini_response(user_input, resources.get('gemini_model'))
            
            # Update tokens
            st.session_state.token_count += len(response.split())
            
            # Add assistant response
            with st.chat_message("assistant", avatar="🏫"):
                st.markdown(f'<div class="message-content">{response}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()