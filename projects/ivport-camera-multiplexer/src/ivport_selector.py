"""Six-camera GPIO selector reconstructed from the original IVPort cascade.

Pin numbers use Raspberry Pi physical BOARD numbering, matching the 2017 build.
"""

import time
import RPi.GPIO as GPIO

BOARD_PINS = {
    "board1": (7, 26, 33),
    "board2": (37, 38, 40),
    "board3": (35, 32, 36),
}

# State tuples are (enable, select_a, select_b).
# Only boards required for a given route are changed by that route.
ROUTES = {
    1: {"board1": (True, True, False), "board2": (False, False, True)},
    2: {"board1": (True, True, False), "board2": (True, False, True)},
    3: {"board1": (True, True, False), "board2": (False, True, False)},
    4: {
        "board1": (True, True, False),
        "board2": (True, True, False),
        "board3": (False, True, False),
    },
    5: {
        "board1": (True, True, False),
        "board2": (True, True, False),
        "board3": (True, True, False),
    },
    6: {"board1": (True, False, True)},
}


class IVPortSelector:
    def __init__(self, settle_seconds=0.1):
        self.settle_seconds = settle_seconds
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        for pins in BOARD_PINS.values():
            for pin in pins:
                GPIO.setup(pin, GPIO.OUT)

    @staticmethod
    def _write_board(name, state):
        pins = BOARD_PINS[name]
        for pin, value in zip(pins, state):
            GPIO.output(pin, value)

    def select(self, camera):
        try:
            route = ROUTES[int(camera)]
        except (KeyError, ValueError):
            raise ValueError("camera must be an integer from 1 through 6")

        for board, state in route.items():
            self._write_board(board, state)

        time.sleep(self.settle_seconds)

    def cleanup(self):
        GPIO.cleanup()
