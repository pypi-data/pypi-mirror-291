import RPi.GPIO as GPIO

class Button:
    # Constructor
    def __init__(self, pin_no):
        self.pin_no = pin_no
        # Configure GPIO
        GPIO.setmode(GPIO.BCM)  # Set up BCM GPIO numbering
        GPIO.setup(self.pin_no, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set GPIO as input (button)

    def is_button_pressed(self):
        """
        Checks if the button connected to GPIO is pressed.
        Returns:
            bool: True if the button is pressed, False otherwise.
        """
        return GPIO.input(self.pin_no) == GPIO.HIGH