import os
import time
from collections import namedtuple

from PIL import ImageFont
from gpiozero import Button
from oled.device import ssd1306
from oled.render import canvas
from sense_hat import SenseHat

#####
# Configuration
I2C_PORT = 1
I2C_ADDRESS = 0x3C
FONT_PATH = "./fonts/Super-Mario-World.ttf"
FONT_SIZE = 8
SCREEN_TOP = 16
PADDING_LEFT = 2
PADDING_TOP = 1
PADDING_BOTTOM = 1
PADDING_RIGHT = 2
# Constants
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
FILL_SOLID = 255
FILL_EMPTY = 0


#####
# Tuples
ButtonEvent = namedtuple("ButtonEvent", "pin name action timestamp")
NamedButton = namedtuple("NamedButton", "name button pin")
PinnedCallbacks = namedtuple("PinnedCallbacks", "pin callbacks")
ButtonCallbacks = namedtuple("ButtonCallbacks", "pressed released held")


#####
# Classes
class ButtonManager(object):

    ACTION_PRESSED = "pressed"
    ACTION_RELEASED = "released"
    ACTION_HELD = "held"

    def __init__(self):
        super(ButtonManager, self).__init__()
        self._event_callback = None
        self._button_map = {}

    def add_button(self, pin, name, pull_up=True, bounce_time=None, hold_time=None, hold_repeat=None):
        if self._button_map.has_key(pin):
            existing_button = self._get_button(pin)
            # TODO: Specialize the error used here
            raise ValueError("Pin {} has already been defined as {}".format(pin, existing_button.name))
        # TODO: Reference http://stackoverflow.com/a/21986301/1846662 for a better way to call Button()
        if bounce_time > 0:
            button = Button(pin, pull_up, bounce_time)
        else:
            button = Button(pin, pull_up)
        if hold_time > 0:
            button.hold_time = hold_time
        if type(hold_repeat) is bool:
            button.hold_repeat = hold_repeat
        button.when_activated = self._handle_pressed
        button.when_deactivated = self._handle_released
        button.when_held = self._handle_held
        self._button_map[pin] = NamedButton(name, button, pin)

    @property
    def event_callback(self):
        return self._event_callback

    @event_callback.setter
    def event_callback(self, value):
        self._event_callback = value

    def _get_button(self, pin):
        return self._button_map[pin]

    def _create_event(self, pin, action):
        button = self._get_button(pin)
        timestamp = int(time.time())
        return ButtonEvent(pin, button.name, action, timestamp)

    def _handle_event(self, pin, action):
        if self._event_callback:
            event = self._create_event(pin, action)
            self._event_callback(event)

    def _handle_pressed(self, device):
        self._handle_event(device.pin.number, self.ACTION_PRESSED)

    def _handle_released(self, device):
        self._handle_event(device.pin.number, self.ACTION_RELEASED)

    def _handle_held(self, device):
        self._handle_event(device.pin.number, self.ACTION_HELD)


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
        self.title = title
        self.items = items

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
            self.clear_screen()
            print
            print("Program stopped.")

    def clear_screen(self):
        with canvas(self.screen) as draw:
            # TODO: Work this in to the managed UI system
            draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill=0)

    #####
    def draw(self):
        with canvas(self.screen) as draw:
            draw.setfont(self.font)
            draw.text((PADDING_LEFT, 0), title, fill=FILL_SOLID)
            top = SCREEN_TOP
            i = 1
            for item in items:
                y = top + PADDING_TOP
                bottom = y + FONT_SIZE
                if i == self.position:
                    draw.rectangle((0, top, SCREEN_WIDTH, bottom), fill=FILL_SOLID)
                    draw.text((PADDING_LEFT, y), item, fill=FILL_EMPTY)
                else:
                    draw.text((PADDING_LEFT, y), item, fill=FILL_SOLID)
                top = bottom + PADDING_BOTTOM
                i += 1

    #####
    def input_event(self, event):
        print("Event direction, action, timestamp:")
        print event.pin
        print event.name
        print event.action
        print event.timestamp
        if event.action == ButtonManager.ACTION_PRESSED:
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
        if self.position < len(self.items):
            self.position += 1

    #####
    def on_refresh(self):
        print "Refreshing UI"
        self.draw()


class Sensor(object):

    #####
    def __init__(self):
        super(Sensor, self).__init__()
        self.hat = SenseHat()


#####
# Program init
d = ssd1306(port=I2C_PORT, address=I2C_ADDRESS)
ui = PiUi(d)

title = "Main Menu"
items = ["System Info", "Options", "Reboot"]

ui.set_buttons(27, 5, 17, 22, 12, 6)
ui.set_menu(title, items)
ui.draw()
ui.loop()
