"""Three-board PCA9685 LED controller for the multispectral imaging project."""

import board
import busio
from adafruit_pca9685 import PCA9685

ADDRESSES = (0x40, 0x41, 0x42)
PWM_FREQUENCY_HZ = 1000
CHANNELS_PER_CONTROLLER = 16
MAX_12_BIT = 4095


class LedController:
    """Expose three PCA9685 devices as one 48-channel output bank."""

    def __init__(self, addresses=ADDRESSES, frequency=PWM_FREQUENCY_HZ):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.controllers = [PCA9685(self.i2c, address=a) for a in addresses]
        for controller in self.controllers:
            controller.frequency = frequency

    @property
    def channel_count(self):
        return len(self.controllers) * CHANNELS_PER_CONTROLLER

    def set_output(self, global_channel, duty_12_bit):
        if not 0 <= global_channel < self.channel_count:
            raise ValueError(f"channel must be 0 through {self.channel_count - 1}")
        if not 0 <= duty_12_bit <= MAX_12_BIT:
            raise ValueError(f"duty must be 0 through {MAX_12_BIT}")

        controller_index, local_channel = divmod(
            global_channel, CHANNELS_PER_CONTROLLER
        )
        duty_16_bit = round(duty_12_bit * 65535 / MAX_12_BIT)
        self.controllers[controller_index].channels[local_channel].duty_cycle = (
            duty_16_bit
        )

    def all_off(self):
        for controller in self.controllers:
            for channel in controller.channels:
                channel.duty_cycle = 0

    def close(self):
        self.all_off()
        for controller in self.controllers:
            controller.deinit()
        self.i2c.deinit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
