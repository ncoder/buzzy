from ast import While
from gpiozero import LED,LEDBoard
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()#host='192.168.0.23'
from time import sleep
from signal import pause

#red = LED(17, pin_factory=factory)
#yellow = LED(27, pin_factory=factory)
#white = LED(22, pin_factory=factory)
#blue = LED(23, pin_factory=factory)
#green = LED(24, pin_factory=factory)
leds = LEDBoard(23, 27, 22, 17, 24,  pin_factory=factory)


i = 0
while True:
    sleep(1)
    t = tuple(j == i for j in range(5))
    leds.value = t
    i = (i+1) %5

