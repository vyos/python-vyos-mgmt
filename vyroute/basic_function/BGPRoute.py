# Copyright (c) 2016 Hochikong
def bgp_as(obj, self_as, neighbor, multihop, remote_as, update_source):
    """VyOS BGP router basic setting about AS

    :param obj: A connection object
    :param self_as: The AS number of the router you login
    :param neighbor: The neighbor router address
    :param multihop: The amount of hops
    :param remote_as: The remote AS number
    :param update_source: The update source
    :return: A message
    """
    bgp_multihop_configuration = "set protocols bgp %s neighbor %s ebgp-multihop %s"
    bgp_remote_as_configuration = "set protocols bgp %s neighbor %s remote-as %s"
    bgp_update_source_configuration = "set protocols bgp %s neighbor %s update-source %s"

    try:
        reg = 0
        error_message = []
        obj.sendline(bgp_multihop_configuration % (self_as, neighbor, multihop))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_message.append(obj.before)
            reg += 1
        obj.sendline(bgp_remote_as_configuration % (self_as, neighbor, remote_as))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_message.append(obj.before)
            reg += 1
        obj.sendline(bgp_update_source_configuration % (self_as, neighbor, update_source))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_message.append(obj.before)
            reg += 1
        if reg > 0:
            return error_message
        else:
            return "Result:Configured successfully"
    except Exception as e:
        return e


def bgp_network(obj, self_as, network_range):
    """Add a network to BGP router

    :param obj: A connection object
    :param self_as: The AS number of the router you login
    :param network_range: The target network,don't forget the netmask
    :return: A message
    """
    bgp_network_configuration = "set protocols bgp %s network %s"

    try:
        obj.sendline(bgp_network_configuration % (self_as, network_range))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result:Configured successfully"
    except Exception as e:
        return e


def bgp_router_id(obj, self_as, router_id):
    """Set a router id for the router you login

    :param obj:A connection object
    :param self_as: The AS number of the router you login
    :param router_id: The router id,or you can use the router address as router id
    :return: A message
    """
    bgp_router_id_configuration = "set protocols bgp %s parameters router-id %s"

    try:
        obj.sendline(bgp_router_id_configuration % (self_as, router_id))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result:Configured successfully"
    except Exception as e:
        return e


def bgp_blackhole_route(obj, network_range):
    """Set a blackhole route

    :param obj: A connection object
    :param network_range: The target network,don't forget the netmask
    :return: A message
    """
    bgp_blackhole_configuration = "set protocols static route %s blackhole distance '254' "

    try:
        obj.sendline(bgp_blackhole_configuration % network_range)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result:Configured successfully"
    except Exception as e:
        return e
