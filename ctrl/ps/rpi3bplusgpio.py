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
        gpio_mode = GPIO.getmode()
        if gpio_mode == GPIO.BCM:
            self.logger.debug("GPIO mode is set to BCM (Broadcom SOC channel) numbering")
        else:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__gpio_conf['GPIO_PIN'], GPIO.OUT)

    def turn_outlet_off(self, outlet_number):
        """Turns a specified outlet off in cutter device"""
        self.__verify_outlet_range(outlet_number)
        self.__act_upon_outlet(self.__gpio_conf['GPIO_CUTTER_OFF'])

    def turn_outlet_on(self, outlet_number):
        """Turns a specified outlet on in cutter device"""
        self.__verify_outlet_range(outlet_number)
        self.__act_upon_outlet(self.__gpio_conf['GPIO_CUTTER_ON'])

    def turn_all_outlets_on(self):
        """Turns all outlets on in cutter device."""
        self.__act_upon_outlet(self.__gpio_conf['GPIO_CUTTER_ON'])

    def turn_all_outlets_off(self):
        """Turns all outlets off in cutter device."""
        self.__act_upon_outlet(self.__gpio_conf['GPIO_CUTTER_OFF'])

    def read_outlet(self, outlet_number):
        """Reads the requested outlet from cutter device"""
        return self.read_all_outlets()[self.__verify_outlet_range(outlet_number)]

    def read_all_outlets(self):
        """Reads all outlets from cutter device."""
        _UNIQUE_SLOT_INDEX = 1
        gpio_val = 1 if GPIO.input(self.__gpio_conf['GPIO_PIN']) == GPIO.HIGH else 0
        return {_UNIQUE_SLOT_INDEX: "{}".format(gpio_val)}

    def __verify_outlet_range(self, outlet_number):
        i_onum = None
        try:
            i_onum = int(outlet_number)
        except ValueError as e:
            self.logger.debug(e)
            msg = "incorrect type of outlet indexing, expecting an int"
            raise PsOutletError(msg)
        if i_onum < 1 or i_onum > self.outlet_count:
            raise PsOutletError("requested outlet {0} is out of range".format(
                outlet_number))
        return i_onum


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
