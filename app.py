import streamlit as st
import google.generativeai as genai
from datetime import datetime

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash-lite")

st.set_page_config(page_title="Tune Journal", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
        .main { background-color: #0d0d0d; }
        h1 { color: #d4a0ff; font-family: Georgia, serif; }
        .stTextArea textarea { background-color: #1a1a1a; color: #f0f0f0; border: 1px solid #d4a0ff; }
        .stButton button { background-color: #d4a0ff; color: #0d0d0d; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("🎵 How are you feeling today?")
st.caption("Write anything. No rules.")

entry = st.text_area("", placeholder="Today I feel...", height=200)

if st.button("Find my song"):
    if entry.strip():
        with st.spinner("Feeling the vibes..."):
            prompt = f"""
           
            
            Someone wrote this journal entry: "{entry}"
            
            Match their mood to 4 songs based on Rap,Neo-soul ,RnB,Pop and Jazz specific song from these artists.
            Respond in this format:
            -Genre
            - Song and artist on the first line in bold
            - 2-3 sentences max explaining why this song fits their mood, written like a wise loving friend
            - End with one short empowering sentence
            
            Keep it personal, warm, and poetic. No bullet points in the response.
            """
            response = model.generate_content(prompt)
            
            st.markdown("---")
            st.markdown("### Your songs for today")
            st.markdown(response.text)
            
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "date": datetime.now().strftime("%B %d, %Y"),
                "entry": entry[:80] + "...",
                "response": response.text
            })
    else:
        st.warning("Write something first, even just a few words.")

# if "history" in st.session_state and st.session_state.history:
#     st.markdown("---")
#     st.markdown("### Previous entries")
#     for item in reversed(st.session_state.history[-5:]):
#         with st.expander(item["date"]):
#             st.caption(item["entry"])
#             st.markdown(item["response"])