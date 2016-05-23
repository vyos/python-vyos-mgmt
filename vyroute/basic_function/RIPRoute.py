# author=hochikong
def riproute(obj, data):
    """This method provide a RIP protocols router configuration function

    Parameter data example:
    {'config':['192.168.10.0/24','10.20.10.0/24'],
    }

    :param obj: a connection object
    :param data: a python dictionary
    :return: a python dictionary
    """
    rip_basic_configuration = "set protocols rip network %s"
    redistribute_configuration = "set protocols rip redistribute connected"
    try:
        # Configure RIP router
        for i in data['config']:
            obj.execute(rip_basic_configuration % i)
        obj.execute(redistribute_configuration)
        return {"Result": "Configured successfully"}
    except Exception, e:
        return {"Error": e}

