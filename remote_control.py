import time
from typing import Tuple

global lthrottle
global rthrottle
global freshness
lthrottle = 0
rthrottle = 0
freshness = 0


def getThrottle() -> Tuple[float, float]:

    now = time.time()
    if now < freshness + 1:
        return (lthrottle, rthrottle)
    else:
        return (0, 0)


def forward():
    global lthrottle
    global rthrottle
    global freshness
    lthrottle = 1
    rthrottle = 1
    freshness = time.time()


def backward():
    global lthrottle
    global rthrottle
    global freshness
    lthrottle = -1
    rthrottle = -1
    freshness = time.time()


def left():
    global lthrottle
    global rthrottle
    global freshness
    lthrottle = -1
    rthrottle = 1
    freshness = time.time()


def right():
    global lthrottle
    global rthrottle
    global freshness
    lthrottle = 1
    rthrottle = -1
    freshness = time.time()


def stop():
    global lthrottle
    global rthrottle
    global freshness
    lthrottle = 0
    rthrottle = 0
    freshness = time.time()


opmap = {1: forward, 2: backward, 3: left, 4: right, 5: stop}
