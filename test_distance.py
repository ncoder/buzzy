from gpiozero import DistanceSensor
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()#host='192.168.0.23'

sensor = DistanceSensor(23, 24, pin_factory=factory)

while True:
    print('Distance to nearest object is', sensor.distance, 'm')
    sleep(1)