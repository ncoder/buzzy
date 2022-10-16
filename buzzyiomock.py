class MockMotor:

    def forward(self, t):
        pass

    def backward(self, t):
        pass

    def stop(self):
        pass


class MockSensor:
    #todo
    pass


class MockEncoder:
    steps = 0


LeftMotor = MockMotor()
RightMotor = MockMotor()
FrontSensor = MockSensor()
DownSensor = MockSensor()
LeftMotorSensor = MockEncoder()
RightMotorSensor = MockEncoder()