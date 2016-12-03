import RPi.GPIO as GPIO

GPIO_MODE = GPIO.BCM
BTN_PINS = {
    27: "up",
    5: "down",
    17: "left",
    22: "right",
    6: "back",
    12: "select",
    18: "reboot"
}
LED_PINS = {
    13: "yellow",
    19: "green"
}
GPIO_BOUNCETIME = 200

def my_callback(channel):
    if BTN_PINS.has_key(channel):
        print "Button pressed! pin: {} | button: {}".format(channel, BTN_PINS.get(channel))
    else:
        print "Channel not defined. pin: {}".format(channel)

def setup():
    GPIO.setmode(GPIO_MODE)
    setup_leds()
    setup_btns()

def setup_btns():
    for pin in BTN_PINS:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=my_callback, bouncetime=GPIO_BOUNCETIME)
        # GPIO.add_event_callback(pin, my_callback)

def setup_leds():
    for pin in LED_PINS:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(pin, GPIO.HIGH)

def loop():
    try:
        raw_input()
        print "\nFalling edge detected. Now your program can continue with"
        print "whatever was waiting for a button press."
    except KeyboardInterrupt:
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    GPIO.cleanup()           # clean up GPIO on normal exit

setup()
loop()