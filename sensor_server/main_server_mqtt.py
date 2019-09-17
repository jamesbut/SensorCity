import io
import paho.mqtt.client as mqtt
import numpy as np
import cv2
from movement_detection import MovementDetection

res_width = 160
res_height = 120

# TODO: this shouldn't be a global variable
movement_detection = MovementDetection(res_height, res_width)

def read_image(msg):

    # TODO: This might be overkill, I might be able
    # to use the msg byte stream directly
    img_stream = io.BytesIO()
    img_stream.write(msg.payload)
    img_stream.seek(0)

    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    return img

def on_connect(client, userdata, flags, rc):

    print("Connected with result code " + str(rc))
    client.subscribe("heat-map/rgb-stream")
    client.subscribe("heat-map/rotary-encoder")

def on_message(client, userdata, msg):

    print("Message received")

    if msg.topic == "heat-map/rotary-encoder":
        if msg.payload == b'0':
            movement_detection.increment_heat_map_growth_rate(3)
        if msg.payload == b'1':
            movement_detection.increment_heat_map_growth_rate(-3)

    if msg.topic == "heat-map/rgb-stream":
        print("RGB image received")
        rgb_img = read_image(msg)
        movement_detection.process(rgb_img)

if __name__ == "__main__":

    james_mac_addr = '192.168.1.69'
    sensor_city_addr = 'sensorcity.io'
    mqtt_broker_addr = sensor_city_addr
    mqtt_port = 1883

    client = mqtt.Client()

    print("Connecting..")
    client.connect(mqtt_broker_addr, mqtt_port, 60)
    print("..connected")

    client.on_connect = on_connect
    client.on_message = on_message

    print("Listening..")

    client.loop_forever()

