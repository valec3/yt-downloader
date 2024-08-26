from pytubefix import YouTube
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

class YoutubeDownloader:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(self.url, on_progress_callback=self.get_progress_download)
        self.stream = None
        self.progress_bar = st.empty()  # Crear la barra de progreso aquí
        self.status_message = st.empty()

    def show_title(self):
        st.header(f"🎬 **{self.yt.title}**")
        self.show_thumbnail()
        self.show_streams()

    def show_thumbnail(self):
        # Mostrar miniatura del video
        thumbnail_url = self.yt.thumbnail_url
        response = requests.get(thumbnail_url)
        img = Image.open(BytesIO(response.content))
        st.image(img, width=300)

    def show_streams(self):
        st.subheader("Select a Stream")
        streams = self.yt.streams
        stream_options = [f"Resolution: {stream.resolution}, Type: {stream.mime_type}" for stream in streams]
        choice = st.selectbox("Select a stream", stream_options)
        self.stream = streams[stream_options.index(choice)]

    def get_file_size(self):
        return self.stream.filesize / 1000000

    def get_permission_continue(self, file_size):
        st.subheader("Download Details")
        st.write(f"**File Size**: {file_size:.2f} MB")
        st.write(f"**Resolution**: {self.stream.resolution}")

        if st.button("⬇️ Download Video"):
            self.stream.download()
            st.success("✅ Download completed!")
            self.status_message.empty()  # Clear the status message after download

    def get_progress_download(self, stream, chunk, bytes_remaining):
        total_size = self.stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size
        
        if percentage > 1.0:
            percentage = 1.0  
        
        self.progress_bar.progress(percentage)
        self.status_message.info(f"📥 Downloading... {percentage*100:.2f}%")

if __name__ == "__main__":
    st.title("YouTube Video Downloader")
    st.write("Paste the URL of the YouTube video you want to download.")

    url = st.text_input("Video URL:")
    if url:
        downloader = YoutubeDownloader(url)
        downloader.show_title()
        if downloader.stream:
            file_size = downloader.get_file_size()
            downloader.get_permission_continue(file_size)
