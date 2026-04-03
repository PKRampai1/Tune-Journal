import streamlit as st
import google.generativeai as genai
from datetime import datetime
import base64

def get_base64_gif(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

gif = get_base64_gif("BG_3.gif")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash-lite")

st.set_page_config(page_title="Tune Journal", page_icon="🎵", layout="centered")

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/gif;base64,{gif}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        h1 {{ color: #d4a0ff; font-family: Georgia, serif; }}
        .stTextArea textarea {{ 
            background-color: rgba(0,0,0,0.6); 
            color: #f0f0f0; 
            border: 1px solid #d4a0ff; 
        }}
        .stButton button {{ 
            background-color: #d4a0ff; 
            color: #0d0d0d; 
            font-weight: bold; 
            width: 100%; 
        }}
        .stMarkdown, .stCaption {{
            color: #f0f0f0;
        }}
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
            st.markdown(f"""
    <div style="
        background-color: rgba(0, 0, 0, 0.7);
        border: 1px solid #d4a0ff;
        border-radius: 12px;
        padding: 20px 25px;
        margin-top: 10px;
    ">
        <p style="color: #d4a0ff; font-size: 14px; margin-bottom: 8px; font-family: Georgia, serif;">✦ Your songs for today</p>
        <p style="color: #f0f0f0; font-size: 16px; line-height: 1.7; margin: 0;">{response.text}</p>
    </div>
""", unsafe_allow_html=True)
            
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