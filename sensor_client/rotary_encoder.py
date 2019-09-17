from RPi import GPIO
from time import sleep

class RotaryEncoder:

    def __init__(self, mqtt_client):

        self.mqtt_client = mqtt_client

        self.clk_growth = 17
        self.dt_growth = 18

        self.clk_decay = 22
        self.dt_decay = 23

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.clk_growth, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt_growth, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.clk_decay, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt_decay, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.growth_counter = 0
        self.decay_counter = 0
        self.clk_growth_last_state = GPIO.input(self.clk_growth)
        self.clk_decay_last_state = GPIO.input(self.clk_decay)


    def listen(self):

        try:

            while True:

                clk_growth_state = GPIO.input(self.clk_growth)
                dt_growth_state = GPIO.input(self.dt_growth)

                if clk_growth_state != self.clk_growth_last_state:
                    if dt_growth_state != clk_growth_state:
                        self.growth_counter += 1
                        self.mqtt_client.publish("heat-map/rotary-encoder/growth_rate", 1)
                    else:
                        self.growth_counter -= 1
                        self.mqtt_client.publish("heat-map/rotary-encoder/growth_rate", 0)
                    print("Growth counter:", self.growth_counter)

                clk_decay_state = GPIO.input(self.clk_decay)
                dt_decay_state = GPIO.input(self.dt_decay)

                if clk_decay_state != self.clk_decay_last_state:
                    if dt_decay_state != clk_decay_state:
                        self.decay_counter += 1
                        self.mqtt_client.publish("heat-map/rotary-encoder/decay_rate", 1)
                    else:
                        self.decay_counter -= 1
                        self.mqtt_client.publish("heat-map/rotary-encoder/decay_rate", 0)
                    print("Decay counter:", self.decay_counter)

                self.clk_growth_last_state = clk_growth_state
                self.clk_decay_last_state = clk_decay_state
                sleep(0.01)

        finally:

            GPIO.cleanup()
