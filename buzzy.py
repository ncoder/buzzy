import asyncio
from time import sleep

from gpiozero import Motor

from buzzyio import LeftMotor, LeftMotorSensor, RightMotor, RightMotorSensor
#from buzzyiomock import (LeftMotor, LeftMotorSensor, RightMotor, RightMotorSensor)
from remote_control import getThrottle
from server import listenForRemoteInput


def forward():
    LeftMotor.forward()
    RightMotor.forward()


def go(m: Motor, s: float):
    """  
		s positive => forward
		s negative => backward
	"""
    if s > 0:
        m.forward(s)
    elif s < 0:
        m.backward(-s)
    else:
        m.stop()


def moveTo(ldist: int, rdist: int):
    ls = 1
    rs = 1
    if ldist < 0:
        ls = -1
        ldist = -ldist
    if rdist < 0:
        rs = -1
        rdist = -rdist

    LeftMotorSensor.steps = 0
    RightMotorSensor.steps = 0
    while abs(LeftMotorSensor.steps) < ldist and abs(
            RightMotorSensor.steps) < rdist:
        print("L" + str(LeftMotorSensor.steps), " R:",
              str(RightMotorSensor.steps))

        if abs(LeftMotorSensor.steps) < abs(RightMotorSensor.steps):
            go(RightMotor, ls * 0.9)  #slow down right motor a bit
            go(LeftMotor, ls)
        elif abs(LeftMotorSensor.steps) > abs(RightMotorSensor.steps):
            go(LeftMotor, ls * 0.9)  #slow down left motor a bit
            go(RightMotor, rs)
        else:
            #normal operation
            go(LeftMotor, ls)
            go(RightMotor, rs)
        sleep(0.001)

    LeftMotor.stop()
    RightMotor.stop()


def backward():
    LeftMotor.backward()
    RightMotor.backward()


def left():
    LeftMotor.backward()
    RightMotor.forward()


def right():
    LeftMotor.forward()
    RightMotor.backward()


def stop():
    LeftMotor.stop()
    RightMotor.stop()


def printSensors():
    print("L" + str(LeftMotorSensor.steps), " R:", str(RightMotorSensor.steps))


async def readControls():
    #LeftMotorSensor.steps = 0
    #RightMotorSensor.steps = 0
    lastlt = 0
    lastrt = 0
    while True:
        # print("L" + str(LeftMotorSensor.steps), " R:",
        #       str(RightMotorSensor.steps))

        lt, rt = getThrottle()

        if lt != lastlt or rt != lastrt:
            print("throttle: " + str(lt) + " " + str(rt))
            lastlt = lt
            lastrt = rt

        go(LeftMotor, lt)
        go(RightMotor, rt)
        await asyncio.sleep(0.001)


# forward 1000 steps
# moveTo(1000,1000)
# backward 1000 steps
# moveTo(-1000,-1000)

# turn left
#moveTo(100,-100)

# starts a remote www client frontend, and listens for websocket commands.
asyncio.get_event_loop().run_until_complete(listenForRemoteInput())
asyncio.get_event_loop().run_until_complete(readControls())

asyncio.get_event_loop().run_forever()
