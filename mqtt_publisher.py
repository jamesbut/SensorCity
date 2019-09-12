import paho.mqtt.client as mqtt

client = mqtt.Client()
print("Connecting..")
client.connect("sensorcity.io", 1883, 60)
print("..connected")

img_file = open("arena.png", "rb")
file_content = img_file.read()
byte_arr = bytearray(file_content)
print(byte_arr)
client.publish("topic/test", byte_arr, 0)


#client.publish("topic/test", "Hello World!")
client.disconnect()
