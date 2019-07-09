import socket
import struct
import io
#from PIL import Image
import numpy as np
import cv2

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

    finally:

        connection.close()
        server_socket.close()
        print("Sockets closed")

    print("Finished")
