'''
    This piece of code establishes a connection
    with an MQTT broker and subsrcibes to a number
    of topics.
    It listens to these topics and then acts according
    to the name and type of message.
'''

import io
import paho.mqtt.client as mqtt
import numpy as np
import cv2
from movement_detection import MovementDetection

# The resolution of the recorded images - this should
# match the resolution in the client code
res_width = 160
res_height = 120

movement_detection = MovementDetection(res_height, res_width)

# Reads image and converts it to an openCV image
def read_image(msg):

    img_stream = io.BytesIO()
    img_stream.write(msg.payload)
    img_stream.seek(0)

    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    return img

# Listens to topics
def on_connect(client, userdata, flags, rc):

    print("Connected with result code " + str(rc))
    client.subscribe("heat-map/rgb-stream")
    client.subscribe("heat-map/rotary-encoder/growth_rate")
    client.subscribe("heat-map/rotary-encoder/decay_rate")
    client.subscribe("heat-map/rotary-encoder/switch")

# Called when a message is received at any of the subscribed topics
def on_message(client, userdata, msg):

    # Change growth rate
    if msg.topic == "heat-map/rotary-encoder/growth_rate":
        if msg.payload == b'0':
            movement_detection.increment_heat_map_growth_rate(100)
        if msg.payload == b'1':
            movement_detection.increment_heat_map_growth_rate(-100)

    # Change decay rate
    if msg.topic == "heat-map/rotary-encoder/decay_rate":
        if msg.payload == b'0':
            movement_detection.increment_heat_map_decay_rate(100)
        if msg.payload == b'1':
            movement_detection.increment_heat_map_decay_rate(-100)

    # Reset heat map rates because switch was pressed
    if msg.topic == "heat-map/rotary-encoder/switch":
        movement_detection.reset_heat_map_rates()

    # Process image and detect movement
    if msg.topic == "heat-map/rgb-stream":
        rgb_img = read_image(msg)
        movement_detection.process(rgb_img)

if __name__ == "__main__":

    # MQTT broker address and port
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

