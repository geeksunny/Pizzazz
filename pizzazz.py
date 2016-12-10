from sense_hat import SenseHat

from pizzazz.ui import PiUi
from pizzazz.display import SSD1306

##########
# ssd1306 driver used is from - https://ssd1306.readthedocs.io/en/latest/
##########

# Configuration
I2C_ADDRESS = 0x3C#, 0x3D


class Sensor(object):

    #####
    def __init__(self):
        super(Sensor, self).__init__()
        self.hat = SenseHat()


#####
# Program init
d = SSD1306(I2C_ADDRESS)
ui = PiUi(d)

title = "Main Menu"
items = ["System Info", "Options", "Reboot"]

ui.set_buttons(27, 5, 17, 22, 12, 6)
ui.set_menu(title, items)
ui.draw()
ui.loop()
