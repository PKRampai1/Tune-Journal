import streamlit as st
from groq import Groq
from datetime import datetime
import base64

def get_base64_gif(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

gif = get_base64_gif("BG_3.gif")

def get_response(entry):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    prompt = f"""
Someone wrote this journal entry: "{entry}"

Match their mood to 10 songs across Rap, Neo-soul, R&B, Pop and Jazz and a song from Sade and a song from Kanye West and a song from Solange, and a song from Beyonce.
Dont be motivational just pick songs that match the vibe of the text provided.
For each song respond in this EXACT format and nothing else:

group the Sade, Beyonce, solange and kanye songs together put a Special mention tag in the Note and put these songs last


GENRE: [genre]
SONG: [song name]
ARTIST: [artist name]
NOTE:Shic: Special Mention(For Sade, Beyonce, solange and kanye songs only)
[2-3 sentences explaining why, written like a wise loving friend. End with one short empowering sentence.]

Repeat this block 10 times, one per song. No bullet points, no extra text.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
    return response.choices[0].message.content

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
            text = get_response(entry)

            songs = []
            blocks = text.strip().split("\n\n")
            for block in blocks:
                lines = block.strip().split("\n")
                song_data = {}
                for line in lines:
                    if line.startswith("GENRE:"):
                        song_data["genre"] = line.replace("GENRE:", "").strip()
                    elif line.startswith("SONG:"):
                        song_data["song"] = line.replace("SONG:", "").strip()
                    elif line.startswith("ARTIST:"):
                        song_data["artist"] = line.replace("ARTIST:", "").strip()
                    elif line.startswith("NOTE:"):
                        song_data["note"] = line.replace("NOTE:", "").strip()
                if len(song_data) == 4:
                    songs.append(song_data)

            for s in songs:
                spotify_url = f"https://open.spotify.com/search/{(s['song'] + ' ' + s['artist']).replace(' ', '%20')}"
                st.markdown(f"""
                    <div style="
                        background-color: rgba(0, 0, 0, 0.7);
                        border: 1px solid #d4a0ff;
                        border-radius: 12px;
                        padding: 20px 25px;
                        margin-top: 16px;
                    ">
                        <p style="color: #888; font-size: 12px; margin: 0 0 4px 0; text-transform: uppercase; letter-spacing: 1px;">{s.get('genre', '')}</p>
                        <p style="color: #d4a0ff; font-size: 18px; font-weight: bold; margin: 0 0 4px 0;">{s.get('song', '')}</p>
                        <p style="color: #aaa; font-size: 14px; margin: 0 0 12px 0;">{s.get('artist', '')}</p>
                        <p style="color: #f0f0f0; font-size: 15px; line-height: 1.7; margin: 0 0 16px 0;">{s.get('note', '')}</p>
                        <a href="{spotify_url}" target="_blank" style="
                            display: inline-block;
                            background-color: #1DB954;
                            color: #000000;
                            padding: 8px 18px;
                            border-radius: 20px;
                            text-decoration: none;
                            font-weight: bold;
                            font-size: 13px;
                        ">▶ Listen on Spotify</a>
                    </div>
                """, unsafe_allow_html=True)

            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "date": datetime.now().strftime("%B %d, %Y"),
                "entry": entry[:80] + "...",
                "response": text
            })
    else:
        st.warning("Write something first, even just a few words.")