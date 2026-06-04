import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NPF AI Intelligence System", page_icon="👮‍♂️", layout="wide")

# --- POLICE BRANDING (Navy Blue, Yellow, Green) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f0f2f6; }}
    [data-testid="stSidebar"] {{ background-color: #002366 !important; color: white !important; }}
    .stButton>button {{ background-color: #FFD700 !important; color: #002366 !important; font-weight: bold !important; border: none !important; }}
    .stMarkdown h1, .stMarkdown h2 {{ color: #002366 !important; }}
    .stTextInput>div>div>input {{ border: 2px solid #002366 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- SECURE AI CONNECTION ---
try:
    # This pulls the key safely from the Streamlit Secrets tab
    # NEVER put the key directly in this code
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # AUTO-DISCOVERY: Find which models this specific key actually supports
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
    
    # Determine a safe default model to avoid 404 errors
    if 'models/gemini-1.5-flash' in available_models:
        DEFAULT_MODEL = 'gemini-1.5-flash'
    elif 'models/gemini-1.5-pro' in available_models:
        DEFAULT_MODEL = 'gemini-1.5-pro'
    elif 'models/gemini-pro' in available_models:
        DEFAULT_MODEL = 'gemini-pro'
    else:
        DEFAULT_MODEL = available_models[0] if available_models else None

except Exception as e:
    st.error("🚨 SECURITY ALERT: API Key not found in Secrets tab.")
    st.info("Please go to Settings -> Secrets and add: GEMINI_API_KEY = 'your_key_here'")
    st.stop()

# --- MODEL MATRIX (Mapping your vision to available models) ---
def get_model_for_usecase(usecase):
    if not DEFAULT_MODEL:
        return None
    
    # If user wants "Pro" or "Think", try to give them Pro, otherwise fallback to default
    if "Pro" in usecase or "Think" in usecase:
        return 'gemini-1.5-pro' if 'models/gemini-1.5-pro' in available_models else DEFAULT_MODEL
    
    # For everything else, try to give them Flash (Fast), otherwise fallback to default
    return 'gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else DEFAULT_MODEL

# --- PERSONAS ---
PROMPTS = {
    "General Assistant": "You are a professional Nigeria Police Force (NPF) Intelligence Officer. Provide precise, formal, and disciplined responses.",
    "Memo Drafter": "You are the NPF Secretariat Lead. Draft formal official memos. Use a bureaucratic, authoritative tone. Always include: SUBJECT, DATE, and ACTION REQUIRED.",
    "Incident Summarizer": "You are a Crime Data Analyst. Summarize incident logs into: 1. Event Summary, 2. Persons of Interest, 3. Critical Risks, and 4. Immediate Recommendations."
}

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Nigeria_Police_Force_Logo.png/640px-Nigeria_Police_Force_Logo.png", width=120)
    st.markdown("<h2 style='color:white; text-align:center;'>NPF COMMAND</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 🧠 Intelligence Level")
    use_case_options = [
        "Complex Research (Pro)", 
        "Deep Logic (Think)", 
        "Real-time Assistant (Flash)", 
        "Massive Data (Flash-Lite)", 
        "Mobile/Privacy (Nano)"
    ]
    model_choice = st.selectbox("Select Use Case", use_case_options)
    
    # Determine the actual model to use based on the Use Case
    selected_model_name = get_model_for_usecase(model_choice)
    
    st.markdown("---")
    st.markdown("### 🎯 Operation Mode")
    mode = st.selectbox("Select Mode", list(PROMPTS.keys()))
    
    st.markdown("---")
    st.markdown(f"🛡️ **Verified Model:** {selected_model_name}")
    st.markdown("🌐 **Network:** Secure Secrets Tunnel")

# --- MAIN UI ---
st.markdown("<h1 style='text-align: center;'>👮‍♂️ NPF Intelligence & Assistance System</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: #006400;'>Active Module: {mode} | Engine: {model_choice}</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Enter police command, report, or query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyzing Intelligence..."):
            try:
                # Create model instance based on the discovery logic
                model = genai.GenerativeModel(selected_model_name)
                full_query = f"{PROMPTS[mode]}\n\nUser Request: {prompt}"
                response = model.generate_content(full_query)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>Official NPF Digital Transformation Initiative | Confidential & Restricted</p>", unsafe_allow_html=True)
