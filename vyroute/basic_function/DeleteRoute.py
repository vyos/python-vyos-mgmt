# Copyright (c) 2016 Hochikong
def deleteroute(obj, route_type):
    """This method provide a router configuration delete function

    Parameter example:
    'rip'/'static'/'ospf'/'bgp'/'all'

    WARNING!
    When you use this function,please don't forget this func will delete all same type
    router configuration,when your 'config' in data is 'rip',it will delete all rip router setting.
    If you do not want your setting disappear,you can delete router configuration manually or rewrite
    this func.

    :param obj: A connection object
    :param route_type: Route type
    :return: A message or an error
    """
    delete_basic_configuration = "delete protocols %s"
    delete_all_protocols = "delete protocols"

    try:
        if route_type == "all":
            obj.sendline(delete_all_protocols)
            obj.prompt()
            if len(obj.before) > obj.before.index('\r\n') + 2:
                return obj.before
            else:
                return "Result : Delete successfully."
        elif route_type == 'rip':
            obj.sendline(delete_basic_configuration % 'rip')
            obj.prompt()
            if len(obj.before) > obj.before.index('\r\n') + 2:
                return obj.before
            else:
                return "Result : Delete successfully."
        elif route_type == 'static':
            obj.sendline(delete_basic_configuration % 'static')
            obj.prompt()
            if len(obj.before) > obj.before.index('\r\n') + 2:
                return obj.before
            else:
                return "Result : Delete successfully."
        elif route_type == 'bgp':
            obj.sendline(delete_basic_configuration % 'bgp')
            obj.prompt()
            if len(obj.before) > obj.before.index('\r\n') + 2:
                return obj.before
            else:
                return "Result : Delete successfully."
        elif route_type == 'ospf':
            obj.sendline(delete_basic_configuration % 'ospf')
            obj.prompt()
            if len(obj.before) > obj.before.index('\r\n') + 2:
                return obj.before
            else:
                return "Result : Delete successfully."
        else:
            return "Error : Nonsupport protocols type."
    except Exception as e:
        return e
