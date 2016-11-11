from oled.device import ssd1306
from oled.render import canvas

d = ssd1306(port=1, address=0x3C)
with canvas(d) as draw:
	draw.rectangle((0,0,128,64), fill=0)
