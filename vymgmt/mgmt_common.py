# Copyright (c) 2016 Hochikong


def messenger(obj, config):
    """This method used for sending configuration to VyOS

    :param obj: A connection object
    :param config: A configuration string
    :return: A message or an error
    """
    try:
        obj.sendline(config)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
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
    try:
        obj.sendline(config)
        obj.prompt()
        if len(obj.before) > obj.before.index('\r\n') + 2:
            return obj.before
        else:
            return "Result : Commit successfully"
    except Exception as e:
        return e
