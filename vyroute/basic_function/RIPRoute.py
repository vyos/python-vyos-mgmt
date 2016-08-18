# Copyright (c) 2016 Hochikong
def rip_network(obj, network_range):
    """This method provide a RIP router network configuration function

    Parameter example:
    '10.20.10.0/24'

    :param obj: A connection object
    :param network_range: The target network,don't forget the netmask
    :return: A message or an error
    """
    rip_basic_configuration = "set protocols rip network %s"

    try:
        # Configure RIP router
        obj.sendline(rip_basic_configuration % network_range)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e


def rip_redistribute(obj):
    """Execute 'set protocols rip redistribute connected' command

    :param obj: A connection object
    :return: A message or an error
    """
    redistribute_configuration = "set protocols rip redistribute connected"

    try:
        obj.sendline(redistribute_configuration)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e
