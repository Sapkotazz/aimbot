from datetime import datetime, timedelta

LOWERING_SERVO_TOP_VALUE = 0.4 #needs to be actually found
LOWERING_SERVO_BOTTOM_VALUE = 0.1 #needs to be actually found

LOWERING_TOTAL_PERIOD = timedelta(seconds=1.6)
LOWERING_PERIOD = timedelta(seconds=0.5)
LOWERING_SERVO_PERIOD = timedelta(seconds=1)

SHOOTING_TOTAL_PERIOD = timedelta(seconds=1)
SHOOTING_SERVO_DOWN_PERIOD = timedelta(seconds=0.4)
SHOOTING_ARM_UP_PERIOD = timedelta(seconds=0.5)

class ShooterService():
  def __init__(self,main_motor,servo,stick):
    self.loweringNextTotal = datetime.now()
    self.loweringNextArm = datetime.now()
    self.loweringNextServo = datetime.now()
    self.shootingTotal = datetime.now()
    self.shootingServoDown = datetime.now()
    self.shootingArmUp = datetime.now()
    self.servo = servo
    self.main_motor = main_motor
    self.lowering = False
    self.shooting = False

  def iterate(self):
    if self.loweringNextTotal > datetime.now():
      self.main_motor.Set(-1)

      if self.loweringNextArm < datetime.now() and self.loweringNextServo < datetime.now():
        self.loweringNextServo = datetime.now() + LOWERING_SERVO_PERIOD
    else:
      self.lowering = False

    if self.loweringNextServo > datetime.now():
      self.servo.Set(LOWERING_SERVO_TOP_VALUE)

    if self.shootingTotal > datetime.now():

      if self.shootingServoDown < datetime.now() and self.shootingArmUp < datetime.now():
        self.shootingArmUp = datetime.now() + SHOOTING_ARM_UP_PERIOD
    else:
      self.shooting = False

    if self.shootingServoDown > datetime.now():
      self.main_motor.Set(-1)
      self.servo.Set(LOWERING_SERVO_BOTTOM_VALUE)

    if self.shootingArmUp > datetime.now():
      self.main_motor.Set(1)

  def lower(self):
    self.loweringNextArm = datetime.now() + LOWERING_PERIOD
    self.loweringNextTotal = datetime.now() + LOWERING_TOTAL_PERIOD
    self.lowering = True

  def shoot(self):
    self.shootingServoDown = datetime.now() + SHOOTING_SERVO_DOWN_PERIOD
    self.shootingTotal = datetime.now() + SHOOTING_TOTAL_PERIOD
    self.shooting = True
