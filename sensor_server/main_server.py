import socket
import struct
import io
from PIL import Image

if __name__ == "__main__":

    # Start listening to socket
    port = 8000

    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    # This waits for data being sent to the socket before executing
    connection = server_socket.accept()[0].makefile('rb')

    try:

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
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream)
            image.show()
            print('Image is %dx%d' % image.size)
            image.verify()
            print('Image is verified')

    finally:
        connection.close()
        server_socket.close()

    print("Finished")
