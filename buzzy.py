from gpiozero import DistanceSensor,Motor,RotaryEncoder
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()#host='192.168.0.23'

""" 
+------------------| |--| |------+
| ooooooooooooo P1 |C|  |A|      |
| 1oooooooooooo    +-+  +-+      |
|    1ooo                        |
| P5 oooo        +---+          +====
|                |SoC|          | USB
|   |D| Pi Model +---+          +====
|   |S| B  V2.0                  |
|   |I|                  |C|+======
|                        |S||   Net
|                        |I|+======
=pwr             |HDMI|          |
+----------------|    |----------+ 


		P1:
			3V3  (1) (2)  5V    
M0			GPIO2  (3) (4)  5V    
M1			GPIO3  (5) (6)  GND   
M2			GPIO4  (7) (8)  GPIO14   MFSG
			GND  (9) (10) GPIO15     MFSY
M3			GPIO17 (11) (12) GPIO18  MBSG
FDE			GPIO27 (13) (14) GND   
FDT			GPIO22 (15) (16) GPIO23  MBSY
			3V3 (17) (18) GPIO24
DDE			GPIO10 (19) (20) GND   
DDT			GPIO9 (21) (22) GPIO25
			GPIO11 (23) (24) GPIO8 
			GND (25) (26) GPIO7 


"""


LeftMotor = Motor(forward=3, backward=2, pin_factory=factory)  #M
RightMotor = Motor(forward=17, backward=4, pin_factory=factory) #M
FrontSensor = DistanceSensor(27, 22, pin_factory=factory)  #FDE, #FDT  #ECHO, #TRG
DownSensor = DistanceSensor(10, 9, pin_factory=factory) #DDE, #DDT
LeftMotorSensor = RotaryEncoder(14, 15, max_steps=0, pin_factory=factory)
RightMotorSensor = RotaryEncoder(23, 18,  max_steps=0, pin_factory=factory)

def forward():
	LeftMotor.forward()
	RightMotor.forward()


def go(m: Motor, s: float):
	"""  
		s positive => forward
		s negative => backward
	"""
	if s >0:
		m.forward(s)
	elif s <0:
		m.backward(-s)
	else:
		m.stop()


def moveTo(ldist:int, rdist:int):
	ls =1
	rs =1
	if ldist < 0:
		ls = -1
		ldist = -ldist
	if rdist < 0:
		rs = -1
		rdist = -rdist

	LeftMotorSensor.steps = 0
	RightMotorSensor.steps = 0
	while abs(LeftMotorSensor.steps) < ldist and abs(RightMotorSensor.steps) < rdist:
		print("L" + str(LeftMotorSensor.steps), " R:", str(RightMotorSensor.steps))

		if abs(LeftMotorSensor.steps) < abs(RightMotorSensor.steps):
			go(RightMotor, ls*0.9)  #slow down right motor a bit
			go(LeftMotor, ls)
		elif abs(LeftMotorSensor.steps) > abs(RightMotorSensor.steps):
			go(LeftMotor, ls*0.9) #slow down left motor a bit
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

# forward 1000 steps
# moveTo(1000,1000)
# backward 1000 steps
# moveTo(-1000,-1000)

# turn left
#moveTo(100,-100)

print("done")

