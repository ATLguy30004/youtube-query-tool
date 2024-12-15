import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Load Hugging Face question-answering pipeline with a better model
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# Function to fetch the transcript from a YouTube video
def get_transcript(video_url):
    try:
        video_id = video_url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item['text'] for item in transcript])
    except Exception as e:
        return f"Error fetching transcript: {e}"

# Function to query the Hugging Face model
def query_transcript(transcript, question):
    try:
        result = qa_pipeline(context=transcript, question=question)
        return result['answer']
    except Exception as e:
        return f"Error with open-source model: {e}"

# Streamlit User Interface
st.title("YouTube Video Query Tool (Improved Open Source)")

video_url = st.text_input("Enter YouTube Video URL:")
question = st.text_input("Ask a question about the video:")

if video_url and question:
    with st.spinner("Fetching transcript and querying..."):
        transcript = get_transcript(video_url)
        if "Error" not in transcript:
            answer = query_transcript(transcript, question)
            st.text_area("Transcript:", transcript, height=200)
            st.success("Answer:")
            st.write(answer)
        else:
            st.error(transcript)
