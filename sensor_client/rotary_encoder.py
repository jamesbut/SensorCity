from RPi import GPIO
from time import sleep

class RotaryEncoder:

    def __init__(self, mqtt_client, mqtt_topic_name, clk_pin, dt_pin, sw_pin):

        self.mqtt_client = mqtt_client
        self.mqtt_topic_name = "heat-map/rotary-encoder/" + mqtt_topic_name

        self.clk = clk_pin
        self.dt = dt_pin
        self.sw = sw_pin

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.counter = 0
        self.clk_last_state = GPIO.input(self.clk)

    def listen(self):

        try:

            while True:

                clk_state = GPIO.input(self.clk)
                dt_state = GPIO.input(self.dt)
                sw_state = GPIO.input(self.sw)

                if clk_state != self.clk_last_state:
                    if dt_state != clk_state:
                        self.counter += 1
                        self.mqtt_client.publish(self.mqtt_topic_name, 1)
                    else:
                        self.counter -= 1
                        self.mqtt_client.publish(self.mqtt_topic_name, 0)

                if sw_state == 0:
                    self.mqtt_client.publish("heat-map/rotary-encoder/switch", 1)

                self.clk_last_state = clk_state
                sleep(0.01)

        finally:

            GPIO.cleanup()
