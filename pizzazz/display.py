from oled.device import ssd1306
from oled.render import canvas
from utils import not_implemented


class AbstractI2CScreen(object):

    # TODO: Work in more of a common interface that uses the PIL objects sent to a master draw() method

    def __init__(self, i2c_address, i2c_port=1):
        self.address = i2c_address
        self.port = i2c_port
        self._device = self._request_device()

    def _request_device(self):
        raise NotImplemented(not_implemented(self, "_request_device()"))

    def clear_screen(self):
        raise NotImplemented(not_implemented(self, "clear_screen()"))

    def screen_width(self):
        raise NotImplemented(not_implemented(self, "screen_width()"))

    def screen_height(self):
        raise NotImplemented(not_implemented(self, "screen_height()"))


class SSD1306(AbstractI2CScreen):

    SCREEN_WIDTH = 128
    SCREEN_HEIGHT = 64
    FILL_SOLID = 255
    FILL_EMPTY = 0

    def _request_device(self):
        return ssd1306(port=self.port, address=self.address)

    def clear_screen(self):
        with canvas(self._device) as draw:
            # TODO: Work this in to the managed UI system
            draw.rectangle((0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT), fill=0)

    def screen_height(self):
        return self.SCREEN_HEIGHT

    def screen_width(self):
        return self.SCREEN_WIDTH


