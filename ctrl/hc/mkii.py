import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for output
output_pin = 18

from ctrl.gen import PsGen
from ctrl.gen import PsHwError, PsOutletError

import struct
import time
import logging
import os

impt_class='MkII'

class MkII(HcGen):
    """
    Control class for a coin hopper 1984
    """
    def __init__(self, logger, *args, **kwargs):
        super().__init__(logger)

# Set up the GPIO pin as an output
GPIO.setup(output_pin, GPIO.OUT)

try:
    while True:
        # Generate a falling edge pulse
        GPIO.output(output_pin, GPIO.HIGH)
        time.sleep(0.005)  # Ensure at least 5 ms pulse duration
        GPIO.output(output_pin, GPIO.LOW)
        
        # Wait for at least 5 ms before generating the next pulse
        time.sleep(0.005)

except KeyboardInterrupt:
    pass

finally:
    # Cleanup GPIO settings
    GPIO.cleanup()
