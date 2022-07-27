import time
import statistics

USE_FAKE_GPIO = True # Chage to FALSE if testing in the Raspberry Pi

if USE_FAKE_GPIO:
    from .fake_gpio import GPIO  # For running app
else:
    import RPi.GPIO as GPIO  # For testing in Raspberry Pi


# import ...

class SensorController:

    def __init__(self):
        self.PIN_TRIGGER = 18  # do not change
        self.PIN_ECHO = 24  # do not change
        self.distance = None
        self.color_from_distance = [False, False, False]
        print('Sensor controller initiated')

    def track_rod(self):

        # ...
        print('Monitoring')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)

        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

        print("Waiting for sensor to settle")

        time.sleep(2)

        print("Calculating distance")

        distance_list = []


        for a in range(10):
            GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)

            time.sleep(0.05)

            GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
            pulse_start_time = 0
            pulse_end_time = 0
            while GPIO.input(self.PIN_ECHO) == 0:
                pulse_start_time = time.time()
            while GPIO.input(self.PIN_ECHO) == 1:
                pulse_end_time = time.time()
            pulse_duration = pulse_end_time - pulse_start_time
            distance = pulse_duration * 17150
            self.distance = round(distance, 2)
            #        self.distance = round(pulse_duration * 17150, 2)
            distance_list.append(self.distance)
        print(distance_list)
        self.distance = statistics.median(distance_list)
        print(self.distance)
        return self.distance

    def get_distance(self):
        return self.distance

    def get_shape_from_distance(self):
        if int(self.distance) in range (14,20):
            self.color_from_distance = [True, False, False]
            return self.color_from_distance
        if int(self.distance) in range(9,15):
            self.color_from_distance = [False, True, False]
            return self.color_from_distance
        if int(self.distance) in range(4, 10):
            self.color_from_distance = [False, False, True]
            return self.color_from_distance
        else:
            return self.color_from_distance
