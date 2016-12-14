import os
from collections import namedtuple
from signal import pause

from PIL import ImageFont

from input import ButtonManager
from mixins import MultiButtonControllerMixin, OkCancelButtonControllerMixin, DPadButtonControllerMixin, \
from utils import not_implemented, is_iterable


MenuItem = namedtuple("MenuItem", "title callback")

DEFAULT_FONT_PATH = "./fonts/Super-Mario-World.ttf"
DEFAULT_FONT_SIZE = 8


class WindowManager(MultiButtonControllerMixin):

    #####
    def __init__(self, left_screen, right_screen):
        super(WindowManager, self).__init__()
        self._btn_mgr = ButtonManager()
        self._btn_mgr.button_controller = self
        self._left_screen = left_screen
        self._right_screen = right_screen
        self._focused_screen = self._left_screen
        self._left_window = None
        self._right_window = None
        self.register_controller(WindowManager.ButtonController(self))

    @property
    def left_window(self):
        return self._left_window

    @left_window.setter
    def left_window(self, value):
        self._left_window = value
        self._left_window.screen = self._left_screen
        self.register_controller(self._left_window)

    @property
    def right_window(self):
        return self._right_window

    @right_window.setter
    def right_window(self, value):
        self._right_window = value
        self._right_window.screen = self._right_screen
        self.register_controller(self._right_window)

    def draw(self):
        if self._left_window is not None:
            self._left_window.refresh()
        if self.right_window is not None:
            self.right_window.refresh()

    #####
    def start(self):
        try:
            print "Main program loop started"
            self.draw()
            pause()
        except KeyboardInterrupt:
            self._cleanup()
            print
            print("Program stopped.")
        else:
            self._cleanup()
            print "Clean exit"

    def _cleanup(self):
        self._left_screen.clear_screen()
        self._right_screen.clear_screen()
    class ButtonController(DPadButtonControllerMixin):
        def __init__(self, window_manager):
            super(WindowManager.ButtonController, self).__init__()
            self._window_manager = window_manager

        def _left_pressed(self):
            print "DOWN"

        def _right_pressed(self):
            print "UP"


class AbstractWindow(object):

    # todo: implement title bar sizing in this class
    # todo: implement needs_refresh logic to prevent unnecessary re-draws

    def __init__(self, window_title, font=DEFAULT_FONT_PATH, font_size=DEFAULT_FONT_SIZE, screen=None):
        super(AbstractWindow, self).__init__()
        self._window_title = window_title
        self._image_font = None
        self.font_size = font_size  # TODO: Need a better way to manage this value
        self.font = font, font_size
        self._screen = screen

    @property
    def title(self):
        return self._window_title

    @title.setter
    def title(self, value):
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
            font_size = DEFAULT_FONT_SIZE
        font_path = os.path.abspath(filename)
        self._image_font = ImageFont.truetype(font_path, font_size)

    def draw(self, screen, image_draw_canvas):
        raise NotImplementedError(not_implemented(self, "draw()"))

    def refresh(self):
         if self._screen is not None:
             self._screen.draw_window(self)

    def _activated(self):
        pass

    def _deactivated(self):
        pass


class MenuWindow(AbstractWindow, DPadButtonControllerMixin, OkCancelButtonControllerMixin):

    # TODO: Move SCREEN_TOP and other header-related code to special class for split-color ssd1306 screens?
    SCREEN_TOP = 16
    PADDING_LEFT = 2
    PADDING_TOP = 1
    PADDING_BOTTOM = 1
    PADDING_RIGHT = 2

    def __init__(self, window_title, font=DEFAULT_FONT_PATH, font_size=DEFAULT_FONT_SIZE, screen=None):
        super(MenuWindow, self).__init__(window_title, font, font_size, screen)
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
        canvas.text((self.PADDING_LEFT, 0), self.title, fill=screen.FILL_SOLID)
        top = self.SCREEN_TOP
        i = 0
        for item in self._menu_items:
            y = top + self.PADDING_TOP
            bottom = y + self.font_size
            if i == self._position:
                canvas.rectangle((0, top, screen.width, bottom), fill=screen.FILL_SOLID)
                canvas.text((self.PADDING_LEFT, y), item.title, fill=screen.FILL_EMPTY)
            else:
                canvas.text((self.PADDING_LEFT, y), item.title, fill=screen.FILL_SOLID)
            top = bottom + self.PADDING_BOTTOM
            i += 1

    def _down_pressed(self):
        self._position = self._position - 1 if self._position > 1 else 1
        self.refresh()

    def _up_pressed(self):
        self._position = self._position - 1 if self._position > 1 else 1
        self.refresh()

    def _ok_pressed(self):
        # TODO: execute callback on selected menu item
        pass

    def _cancel_pressed(self):
        # TODO: go back one item in the history stack
        pass
