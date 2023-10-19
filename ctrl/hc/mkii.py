import struct
import time
import logging
import os
import RPi.GPIO as GPIO

from ctrl.gen import HcGen
from ctrl.gen import HcHwError

impt_class='MkII'

class MkII(HcGen):
    """
    Control class for a coin hopper 1984
    """
    __INTERVAL_MS = 0.005

    def __init__(self, logger, *args, **kwargs):
        super().__init__(logger)

        # Verifies GPIO mode
        gpio_mode = GPIO.getmode()
        if gpio_mode != GPIO.BCM:
            emsg = 'GPIO mode must have been previously set to BCM (Broadcom SOC channel)'
            raise HcHwError(emsg)

        self.logger.debug("GPIO mode set to BCM (Broadcom SOC channel)")

        self._gpio_pin = kwargs.get('gpio_pin', None)
        if not self._gpio_pin:
            raise HcHwError('gpio pin has not been defined')

        # Set up the GPIO pin as an output
        GPIO.setup(self._gpio_pin, GPIO.OUT)

    def dispense(self, quantity):
        """Dispenses a quantity of coins"""
        for i in range(quantity):
            self._falling_edge_pulse(self._gpio_pin)

    @classmethod
    def _falling_edge_pulse(cls, output_pin):
        '''Generates a falling edge pulse'''
        GPIO.output(output_pin, GPIO.HIGH)
        time.sleep(cls.__INTERVAL_MS)  # Ensure pulse duration
        GPIO.output(output_pin, GPIO.LOW)
        time.sleep(cls.__INTERVAL_MS)   # Wait before generating the next pulse
