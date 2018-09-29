import connexion
import six
import math
import redis
import json

from swagger_server.models.joystick import Joystick  # noqa: E501
from swagger_server import util

class Motor:
    def __init__(self, id, x, y, maxSpeed, isFlipped):
        self.id = id
        self.x = x
        self.y = y
        self.maxSpeed = maxSpeed
        self.isFlipped = isFlipped

    def get_turning_speed(self, turningRadius, turningSpeed):
        #return turningSpeed * (turningRadius - self.x) / (self.x**2+self.y**2)
        sign = 1 if self.x > 0 else -1
        return -sign*turningRadius*turningSpeed

    def get_motor_speed(self, turningRadius, turningSpeed, maxTurningSpeed, forwardVel):
        maxTurningSpeed = 1 if maxTurningSpeed == 0 else maxTurningSpeed
        return forwardVel + self.get_turning_speed(turningRadius, turningSpeed)

drivetrain = []
drivetrain.append(Motor(0,-0.4218, 0.53975, 255, False))
drivetrain.append(Motor(1,-0.4218, 0, 255, False))
drivetrain.append(Motor(2,-0.4080, -0.381, 255, False))
drivetrain.append(Motor(3,0.4080, -0.381, 255, False))
drivetrain.append(Motor(4,0.4218, 0, 255, False))
drivetrain.append(Motor(5,0.4218, 0.53975, 255, False))


def make_msg(r_stick_x, r_stick_y):
    turningRadius = -r_stick_x
    sign = -1 if turningRadius < 0 else 1

    forwardVel = 255*r_stick_y

    #vel_mag = math.sqrt(msg.axes[0]**2 + msg.axes[1]**2)
    vel_mag = max(abs(r_stick_x), abs(r_stick_y))
    turningSpeed = (255*vel_mag-abs(forwardVel))
    if turningSpeed > 0:
        turningSpeed = turningSpeed

    # Send raw commands
    turningSpeeds = [0] * len(drivetrain)
    for i in range(len(drivetrain)):
        turningSpeeds[i] = abs(drivetrain[i].get_turning_speed(turningRadius, turningSpeed))

    maxTurningSpeed = max(turningSpeeds)
    speeds = [0] * len(drivetrain)
    for i in range(len(drivetrain)):
        speeds[i] = int(drivetrain[i].get_motor_speed(turningRadius, turningSpeed, maxTurningSpeed, forwardVel))

    cmd = {}
    cmd["type"] = "drive"
    cmd["data"] = speeds
    return cmd

client = redis.StrictRedis(host="rover-core")

def joystick_drive(joystick):  # noqa: E501
    """joystick_drive

     # noqa: E501

    :param joystick: 
    :type joystick: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        joystick = Joystick.from_dict(connexion.request.get_json())  # noqa: E501
    
    print("angle: {} magnitude: {}".format(joystick.angle, joystick.magnitude))

    r_stick_x, r_stick_y = math.cos(joystick.angle) * joystick.magnitude, math.sin(joystick.angle) * joystick.magnitude
    msg = make_msg(r_stick_x, r_stick_y)
    client.publish("joystick", json.dumps(msg))
    
    return
