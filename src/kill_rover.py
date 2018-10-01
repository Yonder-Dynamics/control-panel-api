import connexion
import six
import redis

client = redis.StrictRedis(host='rover-core')

def kill_rover():  # noqa: E501
    """kill_rover

     # noqa: E501


    :rtype: None
    """
    client.publish("kill", "kill")
    return