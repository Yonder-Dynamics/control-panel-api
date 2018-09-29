import connexion
import six

from swagger_server.models.joystick import Joystick  # noqa: E501
from swagger_server import util


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
    
    return