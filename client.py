import os
import streamlit as st
from socket import *

CHUNKSIZE = 1_000_000

# Streamlit UI for selecting the file to upload.
st.title("File Uploader")
filename = st.file_uploader("Select a file", type=["txt", "pdf", "png", "jpg", "jpeg", "mp4", "zip"])

# When the user selects a file and clicks the "Upload" button, establish a socket connection and send the file to the server.
if filename:
    sock = socket()
    sock.connect(('localhost', 5001))
    with sock, filename as f:
        # Send the file name and size to the server.
        sock.sendall(filename.name.encode() + b'\n')
        sock.sendall(f'{os.path.getsize(filename.name)}'.encode() + b'\n')

        # Create a progress bar and initialize it to 0.
        progress_bar = st.progress(0)

        # Send the file in chunks so large files can be handled.
        bytes_sent = 0
        
        while True:
            data = f.read(CHUNKSIZE)
            if not data:
                break
            sock.sendall(data)
            bytes_sent += len(data)

            # Update the progress bar to reflect the current progress.
            progress_bar.progress(bytes_sent / os.path.getsize(filename.name))

    st.success("File uploaded successfully.")
