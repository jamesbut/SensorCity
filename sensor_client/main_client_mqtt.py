import paho.mqtt.client as mqtt
import picamera
import io
import time

if __name__ == "__main__":

    james_mac_addr = '192.168.1.69'
    james_linux_home_addr = '192.168.1.66'
    sensor_city_addr = 'sensorcity.io'
    mqtt_broker_addr = sensor_city_addr
    mqtt_port = 1883

    # Connect to MQTT broker
    client = mqtt.Client()

    print("Connecting..")
    client.connect(mqtt_broker_addr, mqtt_port, 60)
    print("..connected")

    # Set up pi camera
    with picamera.PiCamera() as camera:

        camera.resolution = (640, 480)
        # TODO: Do I need to start preview?
        camera.start_preview()
        time.sleep(2)

        start = time.time()
        stream = io.BytesIO()

        for _ in camera.capture_continuous(stream, 'jpeg'):

            client.publish("heat-map/rgb-stream", stream)

            # Quit if we have been capturing for more than 30s
            if time.time() - start > 30:
                break
