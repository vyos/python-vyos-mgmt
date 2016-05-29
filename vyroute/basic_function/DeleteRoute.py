# Copyright (c) 2016 Hochikong
from Exscript.protocols import SSH2
from Exscript import Account


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
            obj.execute(delete_all_protocols)
            return {"Result": "Delete successfully."}
        elif data['config'] == 'rip':
            obj.execute(delete_basic_configuration % 'rip')
            return {"Result": "Delete successfully."}
        elif data['config'] == 'static':
            obj.execute(delete_basic_configuration % 'static')
            return {"Result": "Delete successfully."}
        elif data['config'] == 'ospf':
            obj.execute(delete_basic_configuration % 'ospf')
            return {"Result": "Delete successfully."}
        else:
            return {"Error": "Nonsupport protocols type."}
    except Exception, e:
        return {"Error": e}