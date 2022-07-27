USE_FAKE_GPIO = True # Chage to FALSE if testing in the Raspberry Pi
import random
from time import sleep


if USE_FAKE_GPIO:
    from .fake_gpio import GPIO  # For running app
else:
    import RPi.GPIO as GPIO  # For testing in Raspberry Pi


# import ...

class MotorController(object):

    def __init__(self):
        self.working = False
        self.stopped = False

    def start_motor(self):
        self.PIN_STEP = 25  # do not change
        self.PIN_DIR = 8  # do not change
        self.working = True
        self.stopped = False
        CW = 1  # clockwise direction
        CCW = 0  # counter clockwise direction
        SPR_CW_360 = 1600 # Steps per Revolution (360 / 0.225) = 1600 clockwise
        SPR_CCW_360 = 1600  # Steps per Revolution (360 / 0.225) = 1600 counter clockwise

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN_DIR, GPIO.OUT)
        GPIO.setup(self.PIN_STEP, GPIO.OUT)

        print('Motor started')
        delay = .000625

        motor_control = random.randint(1, 2)
        if motor_control == 1:
            GPIO.output(self.PIN_DIR, SPR_CW_360)
            for x in range(SPR_CW_360):
                GPIO.output(self.PIN_STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(self.PIN_STEP, GPIO.LOW)
                sleep(delay)
                if self.stopped == True:
                    print("Motor is stopped")
                    break
            print("Rotating 360 degree in clockwise direction")
        if motor_control == 2:
            GPIO.output(self.PIN_DIR, SPR_CCW_360)
            for x in range(SPR_CCW_360):
                GPIO.output(self.PIN_STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(self.PIN_STEP, GPIO.LOW)
                sleep(delay)
                if self.stopped == True:
                    print("Motor is stopped")
                    break
            print("Rotating 360 degree in counter clockwise direction")


        GPIO.cleanup()
        print("Motor is stopped")
        self.working = False


    def stop_motor(self):
        self.stopped = True
        self.working = False

    def is_working(self):
        return self.working
