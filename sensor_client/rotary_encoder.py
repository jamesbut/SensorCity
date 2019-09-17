from RPi import GPIO
from time import sleep

class RotaryEncoder:

    def __init__(self, mqtt_client):

        self.mqtt_client = mqtt_client

        self.clk = 17
        self.dt = 18

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.counter = 0
        self.clk_last_state = GPIO.input(self.clk)


    def listen(self):

        try:

            while True:

                clk_state = GPIO.input(self.clk)
                dt_state = GPIO.input(self.dt)

                if clk_state != self.clk_last_state:
                    if dt_state != clk_state:
                        self.counter += 1
                        self.mqtt_client.publish("heat-map/rotary-encoder", 1)
                    else:
                        self.counter -= 1
                        self.mqtt_client.publish("heat-map/rotary-encoder", 0)
                    print(self.counter)

                self.clk_last_state = clk_state
                sleep(0.01)

        finally:

            GPIO.cleanup()
