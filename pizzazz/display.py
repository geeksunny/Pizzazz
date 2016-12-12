from oled.device import ssd1306
from oled.render import canvas

from utils import not_implemented


class AbstractI2CScreen(object):

    # TODO: Work in more of a common interface that uses the PIL objects sent to a master draw() method
    FILL_SOLID = 255
    FILL_EMPTY = 0

    def __init__(self, i2c_address, i2c_port=1):
        self.address = i2c_address
        self.port = i2c_port
        self._device = self._request_device()

    def _request_device(self):
        raise NotImplemented(not_implemented(self, "_request_device()"))

    @property
    def width(self):
        raise NotImplemented(not_implemented(self, "width()"))

    @property
    def height(self):
        raise NotImplemented(not_implemented(self, "height()"))

    def draw_window(self, window):
        raise NotImplementedError(not_implemented(self, "draw_window()"))

    def clear_screen(self):
        raise NotImplemented(not_implemented(self, "clear_screen()"))


class SSD1306(AbstractI2CScreen):

    __SCREEN_WIDTH = 128
    __SCREEN_HEIGHT = 64

    def _request_device(self):
        return ssd1306(port=self.port, address=self.address)

    def draw_window(self, window):
        with canvas(self._device) as draw:
            window.draw(self, draw)

    def clear_screen(self):
        with canvas(self._device) as draw:
            draw.rectangle((0, 0, self.width, self.height), fill=0)

    @property
    def height(self):
        return self.__SCREEN_HEIGHT

    @property
    def width(self):
        return self.__SCREEN_WIDTH
