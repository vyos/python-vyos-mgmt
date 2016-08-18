# Copyright (c) 2016 Hochikong
def staticroute(obj, network_range, next_hop, distance):
    """This method provide a basic static router configuration function

    Parameter example:
    'network_range':'10.20.10.0/24'
    'next-hop':'10.20.10.1'
    'distance':'1'

    :param obj: A connection object
    :param network_range: The target network,don't forget the netmask
    :param next_hop: The next hop
    :param distance: The distance
    :return: A message or an error
    """
    static_basic_configuration = "set protocols static route %s next-hop %s distance %s"

    try:
        # Configure static router
        obj.sendline(static_basic_configuration % (network_range, next_hop, distance))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e
