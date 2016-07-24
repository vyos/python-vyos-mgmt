# Copyright (c) 2016 Hochikong
def ospfarea(obj, data):
    """This method provide a OSPF area configuration function

    Parameter data example:
    {'config':{'area':'0','network':'192.168.10.0/24'},
    }

    :param obj: a connection object
    :param data: a python dictionary
    :return: a python dictionary
    """
    ospf_basic_configuration = "set protocols ospf area %s network %s"

    try:
        # Configure ospf area
        obj.sendline(ospf_basic_configuration % (data['config']['area'], data['config']['network']))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return {"Result": "Configured successfully"}
    except Exception as e:
        return {"Error": e}


def router_id(obj, data):
    """This method provide a router id configuration function

    Parameter data example:
    {'config':{'id':'1.1.1.1'},
    }

    :param obj: a connection object
    :param data: a python dictionary
    :return: a python dictionary
    """
    router_id_configuration = "set protocols ospf parameters router-id %s"
    try:
        # Configure router id
        obj.sendline(router_id_configuration % data['config']['id'])
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return {"Result": "Configured successfully"}
    except Exception as e:
        return {"Error": e}


def ospf_redistribute(obj, data):
    """This method provide a router redistribute function

    Parameter data example:
    {'config':{'type':'2'},
    }

    :param obj: a connection object
    :param data: a python dictionary
    :return: a python dictionary
    """
    redistribute_configuration = {"0": "set protocols ospf redistribute connected metric-type %s",
                                  "1": "set protocols ospf redistribute connected route-map CONNECT",
                                  }
    try:
        reg = 0
        error_message = []
        obj.sendline(redistribute_configuration['0'] % data['config']['type'])
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
            return {"Result": "Configured successfully"}
    except Exception as e:
        return {"Error": e}


def ospf_adjacency(obj):
    """This method sendline : set protocols ospf log-adjacency-changes

    :param obj: a connection object
    :return: a python dictionary
    """
    log_adjacency_changes_configuration = "set protocols ospf log-adjacency-changes"
    try:
        obj.sendline(log_adjacency_changes_configuration)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return {"Result": "Configured successfully"}
    except Exception as e:
        return {"Error": e}


def ospf_default_route(obj, data):
    """This method sendline : set protocols ospf default-information originate always
    and other commands

    Parameter data example:
    {'config':{'metric':'10','metric-type':'2'},
    }

    :param obj: a connection object
    :param data: a python dictionary
    :return: a python dictionary
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
        obj.sendline(default_route_configuration['1'] % data['config']['metric'])
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        obj.sendline(default_route_configuration['2'] % data['config']['metric-type'])
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        if reg > 0:
            return error_messsage
        else:
            return {"Result": "Configured successfully"}
    except Exception as e:
        return {"Error": e}


def ospf_route_map(obj, data):
    """This method used for VyOS route-map setting when you configure a OSPF router

    Parameter data example:
    {'config':{'rule':'10','interface':'lo'},
    }

    :param obj: a connection object
    :param data: a python dictionary
    :return: a python dictionary
    """
    route_map_configuration = {"0": "set policy route-map CONNECT rule %s action permit",
                               "1": "set policy route-map CONNECT rule %s match interface %s",
                               }
    try:
        reg = 0
        error_messsage = []
        obj.sendline(route_map_configuration['0'] % data['config']['rule'])
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        obj.sendline(route_map_configuration['1'] % (data['config']['rule'], data['config']['interface']))
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        if reg > 0:
            return error_messsage
        else:
            return {"Result": "Configured successfully"}
    except Exception as e:
        return {"Error": e}
