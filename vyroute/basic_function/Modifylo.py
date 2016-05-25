# author=Hochikong
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
        obj.execute(lo_basic_configuration % data['config'])
        return {"Result": "Modify successfully."}
    except Exception, e:
        return {'Error': e}
