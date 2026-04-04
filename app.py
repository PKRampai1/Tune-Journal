import streamlit as st
import google.generativeai as genai
from datetime import datetime
import base64

def get_base64_gif(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

gif = get_base64_gif("BG_3.gif")

def get_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel("gemini-2.5-flash-lite")

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
            
            Match their mood to 4 songs across Rap, Neo-soul, R&B, Pop and Jazz.
            For each song respond in this format:
            Genre
            Song and artist in bold
            2-3 sentences explaining why this song fits their mood, written like a wise loving friend.
            End with one short empowering sentence.
            
            Keep it personal, warm, and poetic. No bullet points.
            """
            model = get_model()
            response = model.generate_content(prompt)
            song_query = response.text.split("\n")[0].replace("**", "").strip()
            spotify_url = f"https://open.spotify.com/search/{song_query.replace(' ', '%20')}"

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
                    <a href="{spotify_url}" target="_blank" style="
                        display: inline-block;
                        margin-top: 16px;
                        background-color: #1DB954;
                        color: #000000;
                        padding: 10px 20px;
                        border-radius: 20px;
                        text-decoration: none;
                        font-weight: bold;
                        font-size: 14px;
                    ">▶ Listen on Spotify</a>
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