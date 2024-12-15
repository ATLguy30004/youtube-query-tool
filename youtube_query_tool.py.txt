import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai

# OpenAI API Key (replace with your API key)
openai.api_key = "YOUR_API_KEY"

def get_transcript(video_url):
    try:
        video_id = video_url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        return f"Error fetching transcript: {e}"

def query_chatgpt(transcript, question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that answers questions based on video transcripts."},
                {"role": "user", "content": f"Transcript: {transcript}\n\nQuestion: {question}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error with ChatGPT API: {e}"

# Streamlit UI
st.title("YouTube Video Query Tool")
video_url = st.text_input("Enter YouTube Video URL:")
question = st.text_input("Ask a question about the video:")

if video_url and question:
    with st.spinner("Fetching transcript and querying..."):
        transcript = get_transcript(video_url)
        if "Error" not in transcript:
            answer = query_chatgpt(transcript, question)
            st.text_area("Transcript:", transcript, height=200)
            st.success("Answer:")
            st.write(answer)
        else:
            st.error(transcript)
