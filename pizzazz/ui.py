import os
from collections import namedtuple
from signal import pause

from PIL import ImageFont

from input import ButtonManager
from mixins import MultiButtonControllerMixin, OkCancelButtonControllerMixin, DPadButtonControllerMixin, \
    AlertLEDControllerMixin, LEDControllerMixin
from utils import not_implemented, is_iterable


MenuItem = namedtuple("MenuItem", "title callback")

DEFAULT_FONT_PATH = "./fonts/Super-Mario-World.ttf"
DEFAULT_FONT_SIZE = 8


class WindowManager(MultiButtonControllerMixin):

    # TODO: Dual screen functionality to be moved to optional subclass
    # TODO: Window history/backstack

    def __init__(self, left_screen, right_screen):
        super(WindowManager, self).__init__()
        self._alert_led = AlertLEDControllerMixin(13, "red")
        self._screensaver_led = LEDControllerMixin(19, "green")
        self._btn_mgr = ButtonManager()
        self._btn_mgr.button_controller = self
        self._left_screen = left_screen
        self._right_screen = right_screen
        self._focused_screen = None
        self._left_window = None
        self._right_window = None
        self._focused_window = None
        self.register_controller(WindowManager.ButtonController(self))

    @property
    def left_window(self):
        return self._left_window

    @left_window.setter
    def left_window(self, value):
        self._left_window = value
        self._left_window.screen = self._left_screen
        if self._focused_screen is None:
            self._focus_screen(self._left_screen)

    @property
    def right_window(self):
        return self._right_window

    @right_window.setter
    def right_window(self, value):
        self._right_window = value
        self._right_window.screen = self._right_screen
        if self._focused_screen is None:
            self._focus_screen(self._right_screen)

    def focus_left(self):
        self._focus_screen(self._left_screen)

    def focus_right(self):
        self._focus_screen(self._right_screen)

    def _focus_screen(self, screen):
        if self._focused_screen is screen:
            return
        self._focused_screen = screen
        if screen is self._left_screen:
            self._focus_window(self._left_window)
        elif screen is self._right_screen:
            self._focus_window(self._right_window)
        else:
            # TODO: Raise exception since we're not expecting this screen
            pass

    def _focus_window(self, window=None):
        if self._focused_window is not None:
            self._focused_window.focused = False
            self.unregister_controller(self._focused_window)
        self._focused_window = window
        if self._focused_window is not None:
            self._focused_window.focused = True
            self.register_controller(self._focused_window)

    def draw(self):
        if self._left_window is not None:
            self._left_window.refresh()
        if self.right_window is not None:
            self.right_window.refresh()

    def start(self):
        try:
            print "Main program loop started"
            self.draw()
            pause()
        except KeyboardInterrupt:
            print("Program stopped.")
        else:
            print "Clean exit"
        finally:
            self._cleanup()

    def _cleanup(self):
        self._left_screen.clear_screen()
        self._right_screen.clear_screen()
        self._btn_mgr.cleanup()
        self._alert_led.close()
        self._screensaver_led.close()

    class ButtonController(DPadButtonControllerMixin):
        def __init__(self, window_manager):
            super(WindowManager.ButtonController, self).__init__()
            self._window_manager = window_manager

        def _left_pressed(self):
            self._window_manager.focus_left()

        def _right_pressed(self):
            self._window_manager.focus_right()


class AbstractWindow(object):

    # todo: implement title bar sizing in this class
    # todo: implement needs_refresh logic to prevent unnecessary re-draws
    # todo: implement _opened and _closed functionality

    def __init__(self, window_title, font=DEFAULT_FONT_PATH, font_size=DEFAULT_FONT_SIZE, screen=None):
        super(AbstractWindow, self).__init__()
        self._window_title = window_title
        self._image_font = None
        self._focused = False
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

    @property
    def focused(self):
        return self._focused

    @focused.setter
    def focused(self, value):
        if type(value) is bool:
            if value != self._focused:
                self._focused = value
                self._when_focused() if self.focused else self._when_unfocused()
                self.refresh()
        else:
            raise TypeError("Expects a boolean value.")

    def _when_focused(self):
        pass

    def _when_unfocused(self):
        pass

    def _when_opened(self):
        pass

    def _when_closed(self):
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
        self._position = -1
        self._menu_items = []
        self._outline = False

    def add_menu_item(self, title, callback, index=None):
        menu_item = MenuItem(title, callback)
        if index is not None:
            self._menu_items.insert(index, menu_item)
        else:
            self._menu_items.append(menu_item)

    def draw(self, screen, canvas):
        canvas.setfont(self.font)
        canvas.text((self.PADDING_LEFT, 0), self.title, fill=screen.fill_solid)
        top = self.SCREEN_TOP
        i = 0
        for item in self._menu_items:
            y = top + self.PADDING_TOP
            bottom = y + self.font_size
            if i == self._position:
                f = screen.fill_empty if self._outline else screen.fill_solid
                o = screen.fill_solid if self._outline else screen.fill_empty
                canvas.rectangle((0, top, screen.width-1, bottom), fill=f, outline=o)
                canvas.text((self.PADDING_LEFT, y), item.title, fill=o)
            else:
                canvas.text((self.PADDING_LEFT, y), item.title, fill=screen.fill_solid)
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
