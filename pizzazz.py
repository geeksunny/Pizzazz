from sense_hat import SenseHat

from pizzazz.ui import MenuWindow, WindowManager
from pizzazz.display import SSD1306

##########
# ssd1306 driver used is from - https://ssd1306.readthedocs.io/en/latest/
##########

# Configuration
I2C_ADDR_LEFT = 0x3D
I2C_ADDR_RIGHT = 0x3C


class Sensor(object):

    #####
    def __init__(self):
        super(Sensor, self).__init__()
        self.hat = SenseHat()


#####
# Program init
screen_left = SSD1306(I2C_ADDR_LEFT)
screen_right = SSD1306(I2C_ADDR_RIGHT)
wm = WindowManager(screen_left, screen_right)

menu_left = MenuWindow("Main Menu")
items_left = ["System Info", "Options", "Reboot"]
for title in items_left:
    menu_left.add_menu_item(title, None)
wm.left_window = menu_left

menu_right = MenuWindow("Special Options")
items_right = ["Come on", "Down to", "South Park"]
for title in items_right:
    menu_right.add_menu_item(title, None)
wm.right_window = menu_right

wm.start()
