import streamlit as st
from google import genai

# --- FAKE PAYWALL LOGIC ---
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

if st.session_state.usage_count >= 3:
    st.warning("⚠️ You have used your 3 free coaching sessions.")
    st.info("To continue, join the waitlist for the Pro plan ($19/month).")
    email = st.text_input("Enter your email for early access:")
    if st.button("Join Waitlist"):
        if email:
            st.success("You're on the list! We'll reach out soon.")
    st.stop() 

# --- PAGE SETUP ---
st.set_page_config(page_title="B2B Sales Coach", page_icon="📞", layout="centered")
st.title("📞 AI Sales Coach for B2B Founders")
st.write("Paste a cold call transcript below. The AI will grade it based on standard B2B SaaS sales frameworks.")

# --- API KEY SETUP ---
api_key = st.text_input("Enter your Gemini API Key (starts with AIza...)", type="password")

# --- THE PROMPT ---
system_prompt = """
You are an expert B2B SaaS Sales Coach. You review cold call transcripts for software founders.
Analyze the transcript and provide:
1. A Score out of 10.
2. What went well.
3. What went wrong.
4. A specific rewrite of their weakest sentence.
Keep it direct and actionable.
"""

# --- UI ---
transcript = st.text_area("Paste your cold call transcript here:", height=300)

if st.button("Grade My Call"):
    if not api_key:
        st.error("Please enter your Gemini API key.")
    elif not transcript:
        st.error("Please paste a transcript first.")
    else:
        with st.spinner("Analyzing call..."):
            try:
                # Initialize the NEW client
                client = genai.Client(api_key=api_key)
                
                # Use the NEW Interactions API syntax
                interaction = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=f"{system_prompt}\n\nTranscript:\n{transcript}"
                )
                
                # Display Result
                st.success("Analysis Complete!")
                st.markdown("### 📊 Feedback")
                st.write(interaction.output_text)
                
                # Increment the counter
                st.session_state.usage_count += 1
                
            except Exception as e:
                st.error(f"Error: {e}")