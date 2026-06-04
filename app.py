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

# --- AI CONNECTION (STABLE VERSION) ---
try:
    # Using the stable generativeai library with your key
    genai.configure(api_key="AQ.Ab8RN6LkjbQZp32SatP9YHe5zFR85CoP39vqWSiCIwlzylf1BQ")
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

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
    mode = st.selectbox("🎯 Operation Mode", list(PROMPTS.keys()))
    st.markdown("---")
    st.markdown("🛡️ **Status:** Stable Cloud Active")
    st.markdown("🌐 **Network:** Hard-Coded Secure Link")

# --- MAIN UI ---
st.markdown("<h1 style='text-align: center;'>👮‍♂️ NPF Intelligence & Assistance System</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: #006400;'>Active Module: {mode}</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter police command, report, or query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyzing Intelligence..."):
            try:
                # Simple logic:Persona + User Input
                full_query = f"{PROMPTS[mode]}\n\nUser Request: {prompt}"
                response = model.generate_content(full_query)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>Official NPF Digital Transformation Initiative | Confidential & Restricted</p>", unsafe_allow_html=True)
