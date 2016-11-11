import os

from PIL import ImageFont
from oled.device import ssd1306
from oled.render import canvas
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_MIDDLE, DIRECTION_RIGHT, DIRECTION_UP
from signal import pause

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
PADDING_LEFT = 2
# Constants
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 64
FILL_SOLID = 255
FILL_EMPTY = 0


#####
class PiUi(object):

    #####
    def __init__(self, screen):
        super(PiUi, self).__init__()
        self.screen = screen
        self.position = 1
        font_path = os.path.abspath(FONT_PATH)
        self.font = ImageFont.truetype(font_path, FONT_SIZE)
        self.sensor = Sensor()
        self.sensor.set_event_handler(self.input_event, self.on_refresh)

    #####
    def set_menu(self, title, items):
        self.title = title
        self.items = items

    def close(self):
        print("Closing joystick!")
        self.sensor.hat.stick.close()

    #####
    def loop(self):
        try:
            if self.loop != None:
                self.loop = True
                while self.loop:
                    self.on_refresh()
                    # self.sensor.wait_for_input()
                    print("Loop:Start")
                    pause()
                    print("Loop:End")
        except KeyboardInterrupt:
            print
            print("Program stopped.")
            self.close()

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
        print(event.direction)
        print(event.action)
        print(event.timestamp)
        if event.action == ACTION_PRESSED:
            if event.direction == DIRECTION_DOWN:
                self.down()
            elif event.direction == DIRECTION_UP:
                self.up()

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
    def refresh(self):
        # self.hat.clear()
        if self.refresh_handler != None:
            self.refresh_handler()

    #####
    def set_event_handler(self, event_handler, refresh_handler=None):
        self.refresh_handler = refresh_handler
        self.hat.stick.direction_up = event_handler
        self.hat.stick.direction_down = event_handler
        self.hat.stick.direction_left = event_handler
        self.hat.stick.direction_right = event_handler
        self.hat.stick.direction_middle = event_handler
        self.hat.stick.direction_any = self.refresh

    #####
    def wait_for_input(self):
        self.hat.stick.wait_for_event(True)
        pause()


### Program init
d = ssd1306(port=I2C_PORT, address=I2C_ADDRESS)
ui = PiUi(d)

title = "Main Menu"
items = ["System Info", "Options", "Reboot"]

ui.set_menu(title, items)
ui.loop()

# ui.close()