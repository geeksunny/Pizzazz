import time
from collections import namedtuple

from gpiozero import Button

# Tuples
ButtonEvent = namedtuple("ButtonEvent", "pin name action timestamp")
NamedButton = namedtuple("NamedButton", "name button pin")
PinnedCallbacks = namedtuple("PinnedCallbacks", "pin callbacks")
ButtonCallbacks = namedtuple("ButtonCallbacks", "pressed released held")

# Constants
ACTION_PRESSED = "pressed"
ACTION_RELEASED = "released"
ACTION_HELD = "held"


class ButtonManager(object):

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
        self._handle_event(device.pin.number, ACTION_PRESSED)

    def _handle_released(self, device):
        self._handle_event(device.pin.number, ACTION_RELEASED)

    def _handle_held(self, device):
        self._handle_event(device.pin.number, ACTION_HELD)

