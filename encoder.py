from config import *

try:
    import RPi.GPIO as GPIO
    HW_AVAILABLE = True
except ImportError:
    HW_AVAILABLE = False


class Encoder:
    def __init__(self):
        self._last_clk = 1
        self._turn = 0
        self._pressed = False

        if HW_AVAILABLE:
            GPIO.setup(PIN_ENC_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(PIN_ENC_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(PIN_ENC_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self._last_clk = GPIO.input(PIN_ENC_CLK)

    def poll(self):
        self._turn = 0
        self._pressed = False

        if not HW_AVAILABLE:
            return

        clk = GPIO.input(PIN_ENC_CLK)
        if clk != self._last_clk and clk == 0:
            dt = GPIO.input(PIN_ENC_DT)
            self._turn = 1 if dt != clk else -1
        self._last_clk = clk

        if GPIO.input(PIN_ENC_SW) == 0:
            self._pressed = True

    def get_turn(self):
        return self._turn

    def get_press(self):
        return self._pressed
