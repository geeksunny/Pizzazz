import os
from collections import namedtuple

from PIL import ImageFont

from input import ButtonManager
from mixins import MultiButtonControllerMixin, PizzazzButtonControllerMixin
from utils import not_implemented, is_iterable


MenuItem = namedtuple("MenuItem", "title callback")


class WindowManager(MultiButtonControllerMixin):

    #####
    def __init__(self, left_screen, right_screen):
        super(WindowManager, self).__init__()
        ButtonManager().button_controller = self
        self.left_screen = left_screen
        self.right_screen = right_screen
        self.focused_screen = self.left_screen

    #####
    def loop(self):
        try:
            raw_input()
        except KeyboardInterrupt:
            self.screen.clear_screen()
            print
            print("Program stopped.")


class AbstractWindow(object):

    DEFAULT_FONT_PATH = "./fonts/Super-Mario-World.ttf"
    DEFAULT_FONT_SIZE = 8

    # todo: implement title bar sizing in this class
    # todo: implement needs_refresh logic to prevent unnecessary re-draws

    def __init__(self, window_title, font=DEFAULT_FONT_PATH, font_size=DEFAULT_FONT_SIZE, screen=None):
        self._window_title = window_title
        self._image_font = None
        self.font = font, font_size
        self._screen = screen

    @property
    def window_title(self):
        return self._window_title

    @window_title.setter
    def window_title(self, value):
        self._window_title = value

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, value):
        self._screen = value

    @property
    def font(self):
        return self._image_font

    @font.setter
    def font(self, value):
        if is_iterable(value):
            filename = value[0]
            font_size = value[1]
        else:
            filename = value
            font_size = self.DEFAULT_FONT_SIZE
        font_path = os.path.abspath(filename)
        self._image_font = ImageFont.truetype(font_path, font_size)

    def draw(self, screen, image_draw_canvas):
        raise NotImplementedError(not_implemented(self, "draw()"))

    def _refresh(self):
         if self._screen is not None:
             self._screen.draw_window(self)


class MenuWindow(AbstractWindow, PizzazzButtonControllerMixin):

    # TODO: Move SCREEN_TOP and other header-related code to special class for split-color ssd1306 screens?
    SCREEN_TOP = 16
    PADDING_LEFT = 2
    PADDING_TOP = 1
    PADDING_BOTTOM = 1
    PADDING_RIGHT = 2

    def __init__(self, window_title):#TODO: Update parameters when finalized
        super(MenuWindow, self).__init__(window_title)
        self._position = 0
        self._menu_items = []

    #####
    def add_menu_item(self, title, callback, index=None):
        menu_item = MenuItem(title, callback)
        if index is not None:
            self._menu_items.insert(index, menu_item)
        else:
            self._menu_items.append(menu_item)

    def draw(self, screen, canvas):
        canvas.setfont(self.font)
        canvas.text((self.PADDING_LEFT, 0), self.window_title, fill=screen.FILL_SOLID)
        top = self.SCREEN_TOP
        i = 1
        for item in self._menu_items:
            y = top + self.PADDING_TOP
            bottom = y + FONT_SIZE
            if i == self._position:
                canvas.rectangle((0, top, screen.width, bottom), fill=screen.FILL_SOLID)
                canvas.text((self.PADDING_LEFT, y), item.title, fill=screen.FILL_EMPTY)
            else:
                canvas.text((self.PADDING_LEFT, y), item.title, fill=screen.FILL_SOLID)
            top = bottom + self.PADDING_BOTTOM
            i += 1

    def _down_pressed(self):
        self._position = self._position - 1 if self._position > 1 else 1
        self._refresh()

    def _up_pressed(self):
        self._position = self._position - 1 if self._position > 1 else 1
        self._refresh()

    def _ok_pressed(self):
        # TODO: execute callback on selected menu item
        pass

    def _cancel_pressed(self):
        # TODO: go back one item in the history stack
        pass
