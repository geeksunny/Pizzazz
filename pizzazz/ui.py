import os

from PIL import ImageFont
from oled.render import canvas

from pizzazz.display import SSD1306
from pizzazz.input import ButtonCallbacks, PinnedCallbacks, ButtonManager, ACTION_PRESSED


FONT_PATH = "./fonts/Super-Mario-World.ttf"
FONT_SIZE = 8
SCREEN_TOP = 16
PADDING_LEFT = 2
PADDING_TOP = 1
PADDING_BOTTOM = 1
PADDING_RIGHT = 2


class PiUi(object):

    BUTTON_UP = "up"
    BUTTON_DOWN = "down"
    BUTTON_LEFT = "left"
    BUTTON_RIGHT = "right"
    BUTTON_OK = "ok"
    BUTTON_CANCEL = "cancel"

    #####
    def __init__(self, screen):
        super(PiUi, self).__init__()
        self.screen = screen
        self.looping = None
        self.position = 1
        font_path = os.path.abspath(FONT_PATH)
        self.font = ImageFont.truetype(font_path, FONT_SIZE)
        # self.sensor = Sensor()
        self._btn_mgr = ButtonManager()
        self._btn_mgr.event_callback = self.input_event
        self._primary_pins = {
            self.BUTTON_UP: None,
            self.BUTTON_DOWN: None,
            self.BUTTON_LEFT: None,
            self.BUTTON_RIGHT: None,
            self.BUTTON_OK: None,
            self.BUTTON_CANCEL: None,
        }
        self._other_pins = {}

    #####
    def set_menu(self, title, items):
        self.menu_title = title
        self.menu_items = items

    #####
    def set_buttons(self, up=0, down=0, left=0, right=0, ok=0, cancel=0):
        self._setup_button(self.BUTTON_UP, up, self.up)
        self._setup_button(self.BUTTON_DOWN, down, self.down)
        self._setup_button(self.BUTTON_LEFT, left)
        self._setup_button(self.BUTTON_RIGHT, right)
        self._setup_button(self.BUTTON_OK, ok)
        self._setup_button(self.BUTTON_CANCEL, cancel)

    def _setup_button(self, name, pin, callback=None):
        if self._primary_pins[name] is not None:
            # TODO: Specialize the error used here
            raise ValueError("Button {} has already been set up on pin {}".format(name, self._primary_pins[name]))
        elif type(pin) is not int:
            raise AttributeError("pin must be an integer")
        else:
            # TODO: Add bounce time and hold logic here
            self._btn_mgr.add_button(pin, name)
            button_callback = ButtonCallbacks(callback, None, None)
            pinned_callback = PinnedCallbacks(pin, button_callback)
            self._primary_pins[name] = pinned_callback

    #####
    def loop(self):
        try:
            raw_input()
        except KeyboardInterrupt:
            self.screen.clear_screen()
            print
            print("Program stopped.")

    #####
    def draw(self):
        with canvas(self.screen._device) as draw:
            draw.setfont(self.font)
            draw.text((PADDING_LEFT, 0), self.menu_title, fill=self.screen.FILL_SOLID)
            top = SCREEN_TOP
            i = 1
            for item in self.menu_items:
                y = top + PADDING_TOP
                bottom = y + FONT_SIZE
                if i == self.position:
                    draw.rectangle((0, top, self.screen.SCREEN_WIDTH, bottom), fill=self.screen.FILL_SOLID)
                    draw.text((PADDING_LEFT, y), item, fill=self.screen.FILL_EMPTY)
                else:
                    draw.text((PADDING_LEFT, y), item, fill=self.screen.FILL_SOLID)
                top = bottom + PADDING_BOTTOM
                i += 1

    #####
    def input_event(self, event):
        print("Event direction, action, timestamp:")
        print event.pin
        print event.name
        print event.action
        print event.timestamp
        if event.action == ACTION_PRESSED:
            if self._primary_pins.has_key(event.name):
                pinned_callback = self._primary_pins[event.name]
                if pinned_callback.callbacks is not None \
                        and pinned_callback.callbacks.pressed is not None:
                    callback = pinned_callback.callbacks.pressed
                    callback()
                else:
                    # TODO: This is so buttons without callbacks will not run the refresh followup. Make this configurable.
                    return
            else:
                return
            # TODO - else if pin is in custom additional button list, self._other_pins
            self.on_refresh()

    #####
    def up(self):
        if self.position > 1:
            self.position -= 1

    #####
    def down(self):
        if self.position < len(self.menu_items):
            self.position += 1

    #####
    def on_refresh(self):
        print "Refreshing UI"
        self.draw()

