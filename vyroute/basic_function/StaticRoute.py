# author=hochikong
def staticroute(obj, data):
    """This method provide a basic static router configuration function

    Parameter data example:
    {'config':[{'target':'10.20.10.0/24','next-hop':'10.20.10.1','distance':'1'},
              {'target':"192.168.20.0/24','next-hop':'192.168.20.1','distance':'1'},
    ],
    }

    :param obj: a connection object
    :param data: a python dictionary
    :return:a python dictionary
    """
    static_basic_configuration = "set protocols static route %s next-hop %s distance %s"

    try:
        # Configure static router
        for i in data['config']:
            obj.execute(static_basic_configuration % (i['target'], i['next-hop'], i['distance']))
        return {"Result": "Configured successfully"}
    except Exception, e:
        return {'Error': e}























