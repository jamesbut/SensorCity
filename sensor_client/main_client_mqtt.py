import paho.mqtt.client as mqtt
import picamera
import io
import time
from rotary_encoder import RotaryEncoder
from multiprocessing import Process
from time import sleep

if __name__ == "__main__":

    sensor_city_addr = 'sensorcity.io'
    mqtt_broker_addr = sensor_city_addr
    mqtt_port = 1883

    res_height = 120
    res_width = 160

    growth_clk_pin = 17
    growth_dt_pin = 18
    growth_sw_pin = 27

    decay_clk_pin = 22
    decay_dt_pin = 23
    decay_sw_pin = 24

    # Connect to MQTT broker
    client = mqtt.Client()

    print("Connecting to MQTT broker..")
    client.connect(mqtt_broker_addr, mqtt_port, 60)
    print("..connected")

    # Start listening to both Rotary Encoders
    growth_rotary_encoder = RotaryEncoder(client, "growth-rate", growth_clk_pin, growth_dt_pin, growth_sw_pin)
    growth_rotary_listener = Process(target=growth_rotary_encoder.listen)
    growth_rotary_listener.start()

    decay_rotary_encoder = RotaryEncoder(client, "decay-rate", decay_clk_pin, decay_dt_pin, decay_sw_pin)
    decay_rotary_listener = Process(target=decay_rotary_encoder.listen)
    decay_rotary_listener.start()

    while True:
        continue

    '''
    # Set up pi camera
    with picamera.PiCamera() as camera:

        camera.resolution = (res_width, res_height)
        camera.start_preview()
        time.sleep(2)

        start = time.time()
        stream = io.BytesIO()

        for _ in camera.capture_continuous(stream, 'jpeg'):

            stream.seek(0)

            client.publish("heat-map/rgb-stream", stream.read())

            # Quit if we have been capturing for more than 30s
            if time.time() - start > 120:
                break

            stream.seek(0)
            stream.truncate()
    '''

    growth_rotary_listener.join()
    decay_rotary_listener.join()
