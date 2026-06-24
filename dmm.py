import time
import numpy as np
from collections import deque
from config import *

try:
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    import RPi.GPIO as GPIO
    HW_AVAILABLE = True
except ImportError:
    HW_AVAILABLE = False


class DMM:
    def __init__(self):
        self.waveform = deque(maxlen=WAVEFORM_SAMPLES)
        self.hold = False
        self.held_reading = 0.0
        self.fuse_blown = False
        self.overload = False
        self._sim_t = 0.0
        self._sim_fuse_blown = False

        if HW_AVAILABLE:
            self._init_hardware()
        else:
            print("Hardware not found — running in simulation mode")

    def _init_hardware(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1115(self.i2c)
        self.ads.data_rate = 860
        self.chan_dcv = AnalogIn(self.ads, ADS.P0)
        self.chan_acv = AnalogIn(self.ads, ADS.P1)
        self.chan_ohm = AnalogIn(self.ads, ADS.P2)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_BUZZER, GPIO.OUT)
        GPIO.output(PIN_BUZZER, GPIO.LOW)
        GPIO.setup(PIN_FUSE_SENSE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(PIN_LED_OVL, GPIO.OUT)
        GPIO.output(PIN_LED_OVL, GPIO.LOW)

    def read(self, mode):
        self._check_fuse()

        if self.hold:
            return self.held_reading

        if self.fuse_blown and mode in (MODE_ACV, MODE_DCV, MODE_SCOPE):
            self.waveform.append(0.0)
            return 0.0

        if mode == MODE_DCV:
            val = self._read_dcv()
        elif mode == MODE_ACV:
            val = self._read_acv()
        elif mode == MODE_OHM:
            val = self._read_ohm()
        elif mode == MODE_CONT:
            val = self._read_continuity()
        elif mode == MODE_SCOPE:
            val = self._read_scope()
        else:
            val = 0.0

        self.overload = self._check_overload(mode, val)
        self._update_ovl_led()
        return val

    def _read_dcv(self):
        if HW_AVAILABLE:
            raw = self.chan_dcv.voltage
            v = raw * DC_DIVIDER_RATIO
        else:
            self._sim_t += 0.02
            v = 12.47 + 0.03 * np.sin(self._sim_t * 2)
        self.waveform.append(v)
        return v

    def _read_acv(self):
        if HW_AVAILABLE:
            samples = []
            for _ in range(100):
                samples.append(self.chan_acv.voltage)
            samples = np.array(samples)
            samples -= np.mean(samples)
            rms = np.sqrt(np.mean(samples ** 2))
            voltage = rms * AC_CALIBRATION
            for s in samples:
                self.waveform.append(s * AC_CALIBRATION)
            return voltage
        else:
            self._sim_t += 0.02
            samples = []
            for i in range(100):
                t = self._sim_t + i / 860.0
                s = 170.0 * np.sin(2 * np.pi * 60 * t)
                samples.append(s)
                self.waveform.append(s)
            rms = np.sqrt(np.mean(np.array(samples) ** 2))
            return rms

    def _read_ohm(self):
        if HW_AVAILABLE:
            v = self.chan_ohm.voltage
        else:
            self._sim_t += 0.02
            v = 1.5 + 0.01 * np.sin(self._sim_t)

        self.waveform.append(v)

        if v >= V_SUPPLY - 0.01:
            return float("inf")
        if v <= 0.01:
            return 0.0
        return R_REFERENCE * v / (V_SUPPLY - v)

    def _read_continuity(self):
        resistance = self._read_ohm()
        if HW_AVAILABLE:
            GPIO.output(PIN_BUZZER, GPIO.HIGH if resistance < CONTINUITY_THRESHOLD else GPIO.LOW)
        return resistance

    def _read_scope(self):
        if HW_AVAILABLE:
            v = self.chan_dcv.voltage * DC_DIVIDER_RATIO
        else:
            self._sim_t += 0.001
            v = 2.5 * np.sin(2 * np.pi * 60 * self._sim_t) + \
                0.8 * np.sin(2 * np.pi * 180 * self._sim_t)
        self.waveform.append(v)
        return v

    def _check_fuse(self):
        if HW_AVAILABLE:
            self.fuse_blown = GPIO.input(PIN_FUSE_SENSE) == 0
        else:
            self.fuse_blown = self._sim_fuse_blown

    def _check_overload(self, mode, val):
        if self.fuse_blown:
            return True
        if mode == MODE_DCV and abs(val) > DC_MAX_VOLTAGE * 0.95:
            return True
        if mode == MODE_ACV and val > AC_CALIBRATION * 0.95:
            return True
        if mode in (MODE_OHM, MODE_CONT) and val == float("inf"):
            return True
        return False

    def _update_ovl_led(self):
        if HW_AVAILABLE:
            GPIO.output(PIN_LED_OVL, GPIO.HIGH if (self.overload or self.fuse_blown) else GPIO.LOW)

    def get_waveform(self):
        return list(self.waveform)

    def toggle_hold(self):
        self.hold = not self.hold
        if self.hold and self.waveform:
            self.held_reading = self.waveform[-1]

    def cleanup(self):
        if HW_AVAILABLE:
            GPIO.output(PIN_BUZZER, GPIO.LOW)
            GPIO.output(PIN_LED_OVL, GPIO.LOW)
            GPIO.cleanup()
