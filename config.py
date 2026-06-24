SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
CYAN = (0, 220, 255)
GRAY = (60, 60, 60)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (120, 120, 120)
ORANGE = (255, 160, 0)

MODE_ACV = 0
MODE_DCV = 1
MODE_OHM = 2
MODE_CONT = 3
MODE_SCOPE = 4

MODE_NAMES = ["VAC", "VDC", "Ω", "CONT", "SCOPE"]

# ADS1115 channel assignments
CH_DCV = 0   # A0: DC voltage through resistor divider
CH_ACV = 1   # A1: ZMPT101B AC voltage transformer output
CH_OHM = 2   # A2: voltage across unknown resistor (series with R_REFERENCE)

# GPIO (BCM numbering)
PIN_BUZZER = 18
PIN_ENC_CLK = 17
PIN_ENC_DT = 27
PIN_ENC_SW = 22
PIN_FUSE_SENSE = 24
PIN_LED_OVL = 25

# DC voltage: R1=150k top, R2=10k bottom -> ratio = (150+10)/10 = 16
DC_DIVIDER_RATIO = 16.0
DC_MAX_VOLTAGE = 50.0

# AC: ZMPT101B calibration (RMS output volts -> mains volts)
AC_CALIBRATION = 240.0

# Resistance: 3.3V through R_REFERENCE in series with unknown, measure across unknown
R_REFERENCE = 10000.0
V_SUPPLY = 3.3

CONTINUITY_THRESHOLD = 50.0

WAVEFORM_SAMPLES = 400

NUM_MODES = 5
