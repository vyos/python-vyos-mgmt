# Copyright (c) 2016 Hochikong
def riproute(obj, data):
    """This method provide a RIP protocols router configuration function

    Parameter data example:
    {'config':'192.168.10.0/24',
    }

    :param obj: a connection object
    :param data: a python dictionary
    :return: a python dictionary
    """
    rip_basic_configuration = "set protocols rip network %s"
    redistribute_configuration = "set protocols rip redistribute connected"
    try:
        # Configure RIP router
        reg = 0
        error_messsage = []
        obj.execute(rip_basic_configuration % data['config'])
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            error_messsage.append(obj.before)
            reg += 1
        obj.execute(redistribute_configuration)
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
