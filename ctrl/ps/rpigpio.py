import RPi.GPIO as GPIO
import time

# Define the GPIO pin you're using to control the relay
relay_pin = 17  # Replace with the actual GPIO pin number you're using

# Set up GPIO mode and initial state
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

try:
    while True:
        # Turn the relay on
        GPIO.output(relay_pin, GPIO.HIGH)
        print("Relay is ON")
        time.sleep(2)  # Keep the relay on for 2 seconds

        # Turn the relay off
        GPIO.output(relay_pin, GPIO.LOW)
        print("Relay is OFF")
        time.sleep(2)  # Keep the relay off for 2 seconds

except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    GPIO.cleanup()  # Cleanup GPIO settings
