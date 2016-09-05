# Copyright (c) 2016 Hochikong

CODEC = 'utf8'


def messenger(obj, config):
    """This method used for sending configuration to VyOS

    :param obj: A connection object
    :param config: A configuration string
    :return: A message or an error
    """
    try:
        obj.sendline(config)
        obj.prompt()
        result = decodetool(obj.before, CODEC)
        if len(result) > result.index('\r\n') + 2:
            return result
        else:
            return "Result : Configured successfully"
    except Exception as e:
        return e


def committer(obj, config):
    """This method used for sending commit task to VyOS

    :param obj: A connection object
    :param config: A configuration string
    :return: A message or an error
    """
    exception_string = "enhanced syslogd: rsyslogd"
    try:
        obj.sendline(config)
        obj.prompt()
        result = decodetool(obj.before, CODEC)
        if len(result) > result.index('\r\n') + 2:
            if exception_string in result:
                return "Result : Commit successfully"
            else:
                return result
        else:
            return "Result : Commit successfully"
    except Exception as e:
        return e


def decodetool(target, codec):
    """This method is used for decoding obj.before to string when run this
    library under python3

    :param target: The obj.before
    :param codec: The codec use to decode
    :return:
    """
    try:
        if type(target) == str:
            return target
        if type(target) == bytes:
            return target.decode(codec)
    except Exception as e:
        return e
