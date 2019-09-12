import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("topic/test")

def on_message(client, userdata, msg):
    print("Hello!")
    print(msg.payload)
    if msg.payload.decode() == "Hello World!":
        print("Yes")
        print(msg.payload.decode())
    else:
        print("No")
        print(msg.payload.decode())

client = mqtt.Client()
client.connect("localhost", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
