# Copyright (c) 2016 Hochikong
def ospfarea(obj, area, network_range):
    """This method provide a OSPF area configuration function

    Parameter example:
    'area':'0'
    'network_range':'192.168.10.0/24'

    :param obj: A connection object
    :param area: The ospf area number
    :param network_range: The target network,don't forget the netmask
    :return: A message or an error
    """
    ospf_basic_configuration = "set protocols ospf area %s network %s"

    try:
        # Configure ospf area
        obj.sendline(ospf_basic_configuration % (area, network_range))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e


def ospf_router_id(obj, router_id):
    """This method provide a router id configuration function

    Parameter example:
    '1.1.1.1'

    :param obj: a connection object
    :param router_id: The router id
    :return: A message or an error
    """
    router_id_configuration = "set protocols ospf parameters router-id %s"
    try:
        # Configure router id
        obj.sendline(router_id_configuration % router_id)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e


def ospf_redistribute(obj, metric_type):
    """This method provide a router redistribute function

    Parameter example:
    '2'

    :param obj: A connection object
    :param metric_type: The metric-type
    :return: A message or an error
    """
    redistribute_configuration = {"0": "set protocols ospf redistribute connected metric-type %s",
                                  "1": "set protocols ospf redistribute connected route-map CONNECT",
                                  }
    try:
        reg = 0
        error_message = []
        obj.sendline(redistribute_configuration['0'] % metric_type)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_message.append(obj.before)
            reg += 1
        obj.sendline(redistribute_configuration['1'])
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_message.append(obj.before)
            reg += 1
        if reg > 0:
            return error_message
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e


def ospf_adjacency(obj):
    """This method execute : set protocols ospf log-adjacency-changes

    :param obj: a connection object
    :return: A message or an error
    """
    log_adjacency_changes_configuration = "set protocols ospf log-adjacency-changes"
    try:
        obj.sendline(log_adjacency_changes_configuration)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e


def ospf_default_route(obj, metric, metric_type):
    """This method execute the commands to configure default route

    Parameter example:
    'metric':'10'
    'metric-type':'2'

    :param obj: A connection object
    :param metric: The metric,a number
    :param metric_type: The metric-type
    :return: A message or an error
    """
    default_route_configuration = {"0": "set protocols ospf default-information originate always",
                                   "1": "set protocols ospf default-information originate metric %s",
                                   "2": "set protocols ospf default-information originate metric-type %s",
                                   }
    try:
        reg = 0
        error_messsage = []
        obj.sendline(default_route_configuration['0'])
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        obj.sendline(default_route_configuration['1'] % metric)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        obj.sendline(default_route_configuration['2'] % metric_type)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        if reg > 0:
            return error_messsage
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e


def ospf_route_map(obj, rule, interface):
    """This method is used for VyOS route-map setting when you configure a OSPF router

    Parameter example:
    'rule':'10'
    'interface':'lo'

    :param obj: A connection object
    :param rule: The route-map rule number
    :param interface: The interface name
    :return: A message or an error
    """
    route_map_configuration = {"0": "set policy route-map CONNECT rule %s action permit",
                               "1": "set policy route-map CONNECT rule %s match interface %s",
                               }
    try:
        reg = 0
        error_messsage = []
        obj.sendline(route_map_configuration['0'] % rule)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        obj.sendline(route_map_configuration['1'] % (rule, interface))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        if reg > 0:
            return error_messsage
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e
