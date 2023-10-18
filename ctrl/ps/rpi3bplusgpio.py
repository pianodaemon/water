import struct
import time
import logging
import os
import RPi.GPIO as GPIO

from ctrl.gen import PsGen
from ctrl.gen import PsHwError, PsOutletError


impt_class='RPi3BPlusGpio'

class RPi3BPlusGpio(PsGen):
    """
    Control class for a Raspberry PI 3 (model B+) gpio relay
    """

    __SLOT_MAX = 1

    def __init__(self, logger, *args, **kwargs):

        super().__init__(logger, self.__SLOT_MAX)

        def det_noc(v):
            if v == self.OUTLET_ON:
                return (self.OUTLET_OFF, self.OUTLET_ON)
            if v == self.OUTLET_OFF:
                return (self.OUTLET_ON, self.OUTLET_OFF)

            raise PsHwError(
                'It was not possible to determine relay behaviour'
            )

        self.__gpio_conf = {
            'GPIO_PIN': kwargs.get('gpio_pin', None),
            'GPIO_CUTTER_ON': None,
            'GPIO_CUTTER_OFF': None
        }

        if not self.__gpio_conf['GPIO_PIN']:
            raise PsError('gpio pin has not been defined')

        self.__gpio_conf['GPIO_CUTTER_ON'], self.__gpio_conf['GPIO_CUTTER_OFF'] = det_noc(
           kwargs.get('gpio_noc', self.OUTLET_ON)
        )


# Set up GPIO mode and initial state
GPIO.setmode(GPIO.BCM)
GPIO.setup(self.__gpio_conf['GPIO_PIN'], GPIO.OUT)

try:
    while True:
        # Turn the relay on
        GPIO.output(self.__gpio_conf['GPIO_PIN'], GPIO.HIGH)
        print("Relay is ON")
        time.sleep(2)  # Keep the relay on for 2 seconds

        # Turn the relay off
        GPIO.output(self.__gpio_conf['GPIO_PIN'], GPIO.LOW)
        print("Relay is OFF")
        time.sleep(2)  # Keep the relay off for 2 seconds

except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    GPIO.cleanup()  # Cleanup GPIO settings
