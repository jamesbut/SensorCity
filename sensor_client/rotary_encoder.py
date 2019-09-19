from RPi import GPIO
from time import sleep

class RotaryEncoder:

    def __init__(self, mqtt_client, mqtt_topic_name, clk_pin, dt_pin, sw_pin):

        self.mqtt_client = mqtt_client
        self.mqtt_topic_name = "heat-map/rotary-encoder/" + mqtt_topic_name

        self.clk = clk_pin
        self.dt = dt_pin
        self.sw = sw_pin

        '''
        self.clk_growth = 17
        self.dt_growth = 18
        self.sw_growth = 27

        self.clk_decay = 22
        self.dt_decay = 23
        self.sw_decay = 24
        '''

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        '''
        GPIO.setup(self.clk_decay, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt_decay, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.sw_decay, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.growth_counter = 0
        self.decay_counter = 0
        self.clk_growth_last_state = GPIO.input(self.clk_growth)
        self.clk_decay_last_state = GPIO.input(self.clk_decay)
        '''

        self.counter = 0
        self.clk_last_state = GPIO.input(self.clk)

    def listen(self):

        try:

            while True:

                '''
                clk_growth_state = GPIO.input(self.clk_growth)
                dt_growth_state = GPIO.input(self.dt_growth)
                sw_growth_state = GPIO.input(self.sw_growth)

                if clk_growth_state != self.clk_growth_last_state:
                    if dt_growth_state != clk_growth_state:
                        self.growth_counter += 1
                        self.mqtt_client.publish("heat-map/rotary-encoder/growth_rate", 1)
                    else:
                        self.growth_counter -= 1
                        self.mqtt_client.publish("heat-map/rotary-encoder/growth_rate", 0)

                clk_decay_state = GPIO.input(self.clk_decay)
                dt_decay_state = GPIO.input(self.dt_decay)
                sw_decay_state = GPIO.input(self.sw_decay)

                if clk_decay_state != self.clk_decay_last_state:
                    if dt_decay_state != clk_decay_state:
                        self.decay_counter += 1
                        self.mqtt_client.publish("heat-map/rotary-encoder/decay_rate", 1)
                    else:
                        self.decay_counter -= 1
                        self.mqtt_client.publish("heat-map/rotary-encoder/decay_rate", 0)

                if sw_growth_state == 0 or sw_decay_state == 0:
                    self.mqtt_client.publish("heat-map/rotary-encoder/switch", 1)

                self.clk_growth_last_state = clk_growth_state
                self.clk_decay_last_state = clk_decay_state
                sleep(0.01)
                '''

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
                    print(self.counter)

                if sw_state == 0:
                    self.mqtt_client.publish("heat-map/rotary-encoder/switch", 1)

                self.clk_last_state = clk_state
                sleep(0.01)

        finally:

            GPIO.cleanup()
