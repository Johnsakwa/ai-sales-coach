import streamlit as st
from google import genai
import tempfile

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Sales Coach | B2B SaaS", layout="wide")

# --- CUSTOM CSS FOR PREMIUM UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Top Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid #333;
        margin-bottom: 0;
    }
    .logo {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.05em;
    }
    .logo span { color: #8b5cf6; }
    
    /* Hero Section with Background Image */
    .hero-container {
        position: relative;
        padding: 6rem 2rem;
        border-radius: 0 0 20px 20px;
        overflow: hidden;
        margin-bottom: 3rem;
        background: linear-gradient(to right, rgba(18, 18, 18, 0.95) 40%, rgba(18, 18, 18, 0.6) 100%), 
                    url('https://images.unsplash.com/photo-1560250097-0b93528c311a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: right center;
        border-bottom: 1px solid #333;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.1;
        color: #ffffff;
        letter-spacing: -0.03em;
        margin-bottom: 1.5rem;
        max-width: 700px;
    }
    .hero-title span { color: #8b5cf6; }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #d4d4d8;
        margin-bottom: 2rem;
        line-height: 1.6;
        max-width: 600px;
    }
    
    /* Inputs & Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #a1a1aa; background-color: transparent; border-bottom: 2px solid transparent; }
    .stTabs [aria-selected="true"] { color: #8b5cf6 !important; border-bottom: 2px solid #8b5cf6 !important; }
    
    .stTextArea textarea {
        background-color: #1e1e24 !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    .stFileUploader { background-color: #1e1e24; border-radius: 12px; padding: 1rem; }
    
    /* Buttons */
    .stButton>button {
        background-color: #8b5cf6;
        color: white;
        border-radius: 30px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stButton>button:hover {
        background-color: #7c3aed;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(139, 92, 246, 0.4);
    }
    
    /* Feedback Card */
    .feedback-card {
        background-color: #1e1e24;
        border: 1px solid #333;
        border-radius: 16px;
        padding: 2rem;
        min-height: 400px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .feedback-card h3 { color: #8b5cf6; margin-top: 0; }
    .feedback-card p, .feedback-card li { color: #d4d4d8; line-height: 1.6; }
    
    /* API Key Input Styling */
    .stTextInput>div>div>input {
        background-color: #1e1e24 !important;
        color: #fff !important;
        border: 1px solid #8b5cf6 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }
    .api-label {
        color: #8b5cf6; 
        font-size: 0.85rem; 
        font-weight: 600; 
        margin-bottom: 5px;
    }
    
    /* Support Section */
    .support-section {
        margin-top: 4rem;
        padding: 2rem;
        background-color: #1e1e24;
        border-radius: 16px;
        border: 1px dashed #8b5cf6;
        text-align: center;
    }
    .support-title { color: #ffffff; font-weight: 600; margin-bottom: 0.5rem; }
    .support-text { color: #a1a1aa; font-size: 0.9rem; margin-bottom: 1rem; }
    .wallet-address {
        background-color: #121212;
        padding: 0.8rem;
        border-radius: 8px;
        font-family: monospace;
        color: #8b5cf6;
        font-weight: bold;
        word-break: break-all;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# --- FAKE PAYWALL LOGIC ---
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

if st.session_state.usage_count >= 3:
    st.warning("You have used your 3 free coaching sessions.")
    st.info("To continue, join the waitlist for the Pro plan ($19/month).")
    email = st.text_input("Enter your email for early access:")
    if st.button("Join Waitlist"):
        if email:
            st.success("You're on the list! We'll reach out soon.")
    st.stop()

# --- TOP NAVIGATION BAR ---
nav_col1, nav_col2, nav_col3 = st.columns([2, 1, 1])

with nav_col1:
    st.markdown('<div class="logo">AI Sales Coach<span>.</span></div>', unsafe_allow_html=True)

with nav_col3:
    st.markdown('<div class="api-label">REQUIRES GEMINI API KEY (FREE)</div>', unsafe_allow_html=True)
    api_key = st.text_input("API Key", type="password", placeholder="Paste API Key Here", label_visibility="collapsed")

# --- HERO SECTION ---
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Close more deals.<br><span>Stop losing on the first call.</span></div>
        <div class="hero-subtitle">
            Upload a recording or paste a transcript. Our AI analyzes your pitch against top B2B SaaS frameworks and gives you brutal, actionable feedback to win more clients.
        </div>
    </div>
""", unsafe_allow_html=True)

# --- MAIN APP LAYOUT ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<h3 style='color: #ffffff;'>1. Input Your Call</h3>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Paste Transcript", "Upload Audio"])
    
    transcript = ""
    
    with tab1:
        transcript = st.text_area("Paste your cold call transcript here:", height=280, placeholder="Founder: Hi John, I saw you're the VP of Sales...\nProspect: Yeah, who is this?\n...")
        
    with tab2:
        uploaded_file = st.file_uploader("Upload a recording (mp3, wav, m4a)", type=["wav", "mp3", "m4a", "ogg"])
        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/wav')
            st.session_state.uploaded_audio = uploaded_file
            st.success("Audio ready for analysis.")
            
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("Analyze My Pitch", use_container_width=True)

with col2:
    st.markdown("<h3 style='color: #ffffff;'>2. AI Feedback</h3>", unsafe_allow_html=True)
    
    system_prompt = """
    You are an expert B2B SaaS Sales Coach. You review cold call transcripts for software founders.
    Analyze the transcript and provide:
    1. A Score out of 10.
    2. What went well.
    3. What went wrong.
    4. A specific rewrite of their weakest sentence.
    Keep it direct and actionable. Format with markdown. Be brutally honest. Do not use emojis.
    """

    if analyze_btn:
        has_audio = "uploaded_audio" in st.session_state and st.session_state.uploaded_audio is not None
        
        if not api_key:
            st.error("Please enter your Gemini API key in the top right corner.")
        elif not transcript and not has_audio:
            st.error("Please paste a transcript or upload an audio file first.")
        else:
            with st.spinner("Analyzing your pitch..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    if has_audio and not transcript:
                        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                        temp_audio.write(st.session_state.uploaded_audio.getvalue())
                        temp_audio.close()
                        
                        audio_file = client.files.upload(file=temp_audio.name)
                        
                        interaction = client.interactions.create(
                            model="gemini-3.8-flash",
                            input=[
                                {"type": "text", "text": system_prompt},
                                {"type": "audio", "uri": audio_file.uri, "mime_type": audio_file.mime_type}
                            ]
                        )
                    else:
                        interaction = client.interactions.create(
                            model="gemini-3.8-flash",
                            input=f"{system_prompt}\n\nTranscript:\n{transcript}"
                        )
                    
                    st.markdown(f"""
                        <div class="feedback-card">
                            {interaction.output_text}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.session_state.usage_count += 1
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.markdown("""
            <div class="feedback-card" style="display: flex; align-items: center; justify-content: center; color: #555;">
                <p>Your AI feedback will appear here.</p>
            </div>
        """, unsafe_allow_html=True)

# --- SUPPORT SECTION (BOTTOM) ---
st.markdown("<hr style='border-color: #333; margin-top: 4rem;'>", unsafe_allow_html=True)
st.markdown("""
    <div class="support-section">
        <div class="support-title">Did this tool help you close a deal?</div>
        <div class="support-text">This tool is free to use. If it saved you from a bad pitch, consider buying me a coffee (or crypto).</div>
        <div class="wallet-address">
            0xa37383c1b1ea77a24d38691dc8dc8b19fc95d581
        </div>
        <div class="support-text" style="margin-top: 10px; font-size: 0.8rem;">Binance / BEP-20 / ERC-20 (BNB or USDT)</div>
    </div>
""", unsafe_allow_html=True)