from oled.device import ssd1306
from oled.render import canvas


class SSD1306(object):

    # TODO: Should some of this be broken out into an AbstractI2CScreen class?

    SCREEN_WIDTH = 128
    SCREEN_HEIGHT = 64
    FILL_SOLID = 255
    FILL_EMPTY = 0

    def __init__(self, i2c_address, i2c_port=1):
        self.address = i2c_address
        self.port = i2c_port
        self._device = self._request_device()

    def _request_device(self):
        return ssd1306(port=self.port, address=self.address)

    def clear_screen(self):
        with canvas(self._device) as draw:
            # TODO: Work this in to the managed UI system
            draw.rectangle((0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), fill=0)

