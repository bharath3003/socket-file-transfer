import streamlit as st
from socket import *
import os

CHUNKSIZE = 1_000_000

# Make a directory for the received files.
os.makedirs('Downloads', exist_ok=True)

# Set up the socket to listen for connections.
sock = socket()
sock.bind(('', 5001))
sock.listen(1)

st.title('File Receiver')

while True:
    # Wait for a connection.
    st.write('Waiting for connection...')
    client, addr = sock.accept()
    st.write(f'Connected to {addr}.')

    # Use a socket.makefile() object to treat the socket as a file.
    # Then, readline() can be used to read the newline-terminated metadata.
    with client, client.makefile('rb') as clientfile:
        filename = clientfile.readline().strip().decode()
        length = int(clientfile.readline())
        st.write(f'Downloading {filename}:{length}...')

        #saving the file in a new folder named downloads
        path = os.path.join('Downloads', filename)

        # Read the data in chunks so it can handle large files.
        with open(path, 'wb') as f:
            while length:
                chunk = min(length, CHUNKSIZE)
                data = clientfile.read(chunk)
                if not data:
                    break  # socket closed
                f.write(data)
                #decrementing the size of the file 
                length -= len(data)
                
        #checking for entire file transfer
        if length != 0:
            st.write('Invalid download.')
        else:
            st.write('download completed.')
