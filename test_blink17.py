from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()#host='192.168.0.23'
from time import sleep

blue = LED(17, pin_factory=factory)

while True:
    blue.on()
    sleep(1)
    blue.off()
    sleep(1)

