from gpiozero import LED,PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()#host='192.168.0.23'
from time import sleep


led = PWMLED(17,pin_factory=factory)

while True:
    led.value = 0  # off
    sleep(1)
    led.value = 0.5  # half brightness
    sleep(1)
    led.value = 1  # full brightness
    sleep(1)
