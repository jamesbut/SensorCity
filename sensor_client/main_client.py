import io
import time
import picamera
import socket
import struct

def establish_connection(host, port):

    print("Establishing connection...")

    # Create client socket to the server
    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Create file-like object out of the connection
    connection = client_socket.makefile('wb')

    print("...connection established")

    return client_socket, connection

def send_images(connection):

    with picamera.PiCamera() as camera:

        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)

        start = time.time()
        stream = io.BytesIO()

        for _ in camera.capture_continuous(stream, 'jpeg'):

            # Write length of the capture to stream and flush
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()

            # Rewind the stream and send the image data
            stream.seek(0)
            connection.write(stream.read())

            # Quit if we have beebn capturing for more than 30s
            if time.time() - start > 30:
                break;

            # Reset the stream for next capture
            stream.seek(0)
            stream.truncate()

    # Write a length of zero to stream to signal we are done
    connection.write(struct.pack('<L', 0))

def send_video(connection):

    with picamera.PiCamera() as camera:

        camera.resolution = (640, 480)
        camera.framerate = 24

        camera.start_preview()
        time.sleep(2)

        # Start recording, sending the output to the connection for 60
        # seconds then stop
        camera.start_recording(connection, format='h264')
        camera.wait_recording(30)
        camera.stop_recording()

if __name__ == "__main__":

    print("Starting...")

    # Either send as video or images
    send_as_video = False

    # Connect client socket to server
    host = '192.168.1.69'
    port = 8000

    client_socket, connection = establish_connection(host, port)

    try:

        if send_as_video:
            send_video(connection)
        else:
            send_images(connection)

    finally:

        connection.close()
        client_socket.close()
