# Copyright (c) 2016 Hochikong
def deleteroute(obj, data):
    """This method provide a router configuration delete function

    Parameter data example:
    {'config':'rip'/'static'/'ospf'/'all'
    }

    WARNING!
    When you use this function,please don't forget this func will delete all same type
    router configuration,when your 'config' in data is 'rip',it will delete all rip router setting.
    If you do not want your setting disappear,you can delete router configuration manually or rewrite
    this func.

    :param obj: a connection object
    :param data: a python dictionary
    :return: a python dictionary
    """
    delete_basic_configuration = "delete protocols %s"
    delete_all_protocols = "delete protocols"

    try:
        if data['config'] == "all":
            obj.sendline(delete_all_protocols)
            obj.prompt()
            if len(obj.before) > obj.before.index('\r\n') + 2:
                return obj.before
            else:
                return {"Result": "Delete successfully."}
        elif data['config'] == 'rip':
            obj.sendline(delete_basic_configuration % 'rip')
            obj.prompt()
            if len(obj.before) > obj.before.index('\r\n') + 2:
                return obj.before
            else:
                return {"Result": "Delete successfully."}
        elif data['config'] == 'static':
            obj.sendline(delete_basic_configuration % 'static')
            obj.prompt()
            if len(obj.before) > obj.before.index('\r\n') + 2:
                return obj.before
            else:
                return {"Result": "Delete successfully."}
        elif data['config'] == 'ospf':
            obj.sendline(delete_basic_configuration % 'ospf')
            obj.prompt()
            if len(obj.before) > obj.before.index('\r\n') + 2:
                return obj.before
            else:
                return {"Result": "Delete successfully."}
        else:
            return {"Error": "Nonsupport protocols type."}
    except Exception as e:
        return {"Error": e}
