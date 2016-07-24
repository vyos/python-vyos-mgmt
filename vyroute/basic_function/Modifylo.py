# Copyright (c) 2016 Hochikong
def modifylo(obj, data):
    """This method provide a loopback address configuration function

    Parameter data example:
    {'config':'1.1.1.1/32'
    }

    :param obj: a connection object
    :param data: a python dictionary
    :return: a python dictionary
    """

    lo_basic_configuration = "set interfaces loopback lo address %s"

    try:
        # Configure loopback interface lo address
        obj.sendline(lo_basic_configuration % data['config'])
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return {"Result": "Modify successfully."}
    except Exception as e:
        return {'Error': e}
