# Copyright (c) 2016 Hochikong
def modifylo(obj, lo_address):
    """This method provide a loopback address configuration function

    Parameter example:
    '1.1.1.1/32'

    :param obj: A connection object
    :param lo_address: The target address you want.Don't forget the netmask
    :return: A message or an error
    """

    lo_basic_configuration = "set interfaces loopback lo address %s"

    try:
        # Configure loopback interface lo address
        obj.sendline(lo_basic_configuration % lo_address)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result : Add successfully."
    except Exception as e:
        return e
