import streamlit as st
from pytube import YouTube
import tempfile
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import librosa
import numpy as np

def download_audio(youtube_url):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    audio_stream.download(filename=temp_audio.name)
    return temp_audio.name

def detect_drop_point(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    hop_length = 512
    energy = np.array([
        sum(abs(y[i:i+hop_length]**2)) for i in range(0, len(y), hop_length)
    ])
    drop_index = np.argmax(energy)
    drop_time = (drop_index * hop_length) / sr
    return drop_time

def cut_video_around_drop(video_path, drop_time, duration=60):
    clip = VideoFileClip(video_path)
    start = max(drop_time, 0)
    end = min(start + duration, clip.duration)
    subclip = clip.subclip(start, end)
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    subclip.write_videofile(temp_video.name, codec="libx264", audio_codec="aac", verbose=False, logger=None)
    return temp_video.name

st.title("Corta clip de DJ set en drop energético para TikTok")

youtube_url = st.text_input("Pon aquí el link de YouTube (DJ Set)")

if youtube_url:
    with st.spinner("Descargando audio..."):
        audio_path = download_audio(youtube_url)

    with st.spinner("Detectando drop energético..."):
        drop_time = detect_drop_point(audio_path)

    st.write(f"Drop detectado alrededor de: {drop_time:.2f} segundos")

    with st.spinner("Descargando video completo para cortar clip..."):
        yt = YouTube(youtube_url)
        video_stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
        video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        video_stream.download(filename=video_path)

    with st.spinner("Cortando clip de 1 minuto alrededor del drop..."):
        clip_path = cut_video_around_drop(video_path, drop_time)

    st.video(clip_path)
    with open(clip_path, "rb") as f:
        btn = st.download_button(label="Descargar clip para TikTok", data=f, file_name="clip_tiktok.mp4", mime="video/mp4")
