Heat Map - Sensor City
------------------

This project records a camera stream from a Raspberry Pi and publishes it to an MQTT broker. The server then reads these images and builds a heat map from them.

There is a client and server part to this code.

#### Client

The code in sensor_client is meant to be pushed to an OpenBalena server. This
code then starts capturing images and recording readings from 2 rotary
encoders. It then publishes this data to an MQTT broker.

When downloaded from the OpenBalena server, the client code should run
automatically.

#### Server

The code in sensor_server reads the data from the MQTT broker and detects
movement in the images - it then builds a heat map from this information. It
also listens for state changes of the rotary encoders and changes the growth and decay rates of the heat map.

##### To run:

python3 main_server_mqtt.py
