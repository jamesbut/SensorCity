'''
    This class listens to input from a rotary encoder.
    It also publishes messages to an MQTT broker based
    upon these inputs.
'''

from RPi import GPIO
from time import sleep

class RotaryEncoder:

    def __init__(self, mqtt_client, mqtt_topic_name, clk_pin, dt_pin, sw_pin):

        self.mqtt_client = mqtt_client
        self.mqtt_topic_name = "heat-map/rotary-encoder/" + mqtt_topic_name

        self.clk = clk_pin
        self.dt = dt_pin
        self.sw = sw_pin

        #Set up GPIO pins
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.clk_last_state = GPIO.input(self.clk)

    def listen(self):

        try:

            while True:

                #Read GPIO states
                clk_state = GPIO.input(self.clk)
                dt_state = GPIO.input(self.dt)
                sw_state = GPIO.input(self.sw)

                #Check for clockwise or anti-clockwise direction
                if clk_state != self.clk_last_state:
                    if dt_state != clk_state:
                        self.mqtt_client.publish(self.mqtt_topic_name, 1)
                    else:
                        self.mqtt_client.publish(self.mqtt_topic_name, 0)

                #Check for switch press
                if sw_state == 0:
                    self.mqtt_client.publish("heat-map/rotary-encoder/switch", 1)

                self.clk_last_state = clk_state
                sleep(0.01)

        finally:

            GPIO.cleanup()
