import socket
import struct
import io
#from PIL import Image
import numpy as np
import cv2
import subprocess

def bind_socket(port):

    # Start listening to socket
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    # This waits for data being sent to the socket before executing
    connection = server_socket.accept()[0].makefile('rb')

    return server_socket, connection

def read_images(connection):

    while True:

        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break

        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))

        # Rewind the stream
        image_stream.seek(0)

        # Open image with PIL and do some processing on it
        #image = Image.open(image_stream)
        #image.show()
        #print('Image is %dx%d' % image.size)
        #image.verify()
        #print('Image is verified')

        # Open image with OpenCV
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        cv2.imshow('Image', img)
        cv2.waitKey(1)

def read_video(connection):

    vlc_command = '/Applications/VLC.app/Contents/MacOS/VLC'

    # Run a viewer with an appropriate command line
    cmdline = [vlc_command, '--demux', 'h264', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)

    try:

        while True:

            # Repeatedly read 1k of data from the content and write it to
            # the media player's stdin
            data = connection.read(1024)
            if not data:
                break
            player.stdin.write(data)

    finally:

        player.terminate()

if __name__ == "__main__":

    # Either receive as images or video
    receive_as_video = True

    port = 8000

    server_socket, connection = bind_socket(port)

    try:

        if receive_as_video:
            read_video(connection)
        else:
            read_images(connection)

    finally:

        connection.close()
        server_socket.close()
        print("Sockets closed")

    print("Finished")
