# author=hochikong
from Exscript.protocols import SSH2
from Exscript import Account


def staticroute(data):
    """This method provide a basic static router configuration function

    Parameter data example:
    {'router':'vyos@172.16.77.188','passwd':'vyos',
    'config':[{'target':'10.20.10.0/24','next-hop':'10.20.10.1','distance':'1'},
              {'target':"192.168.20.0/24','next-hop':'192.168.20.1','distance':'1'}
    ]
    }

    :param data: a python dictionary
    :return:a python dictionary
    """
    basic_configuration = "set protocols static route %s next-hop %s distance %s"

    try:
        stringlist = list(data['router'])
        divi = stringlist.index('@')
        user = ''.join(stringlist[:divi])
        passwd = data['passwd']
        address = ''.join(stringlist[divi+1:])
        account = Account(user, passwd)
        conn = SSH2()
        conn.connect(address)
        conn.login(account)

# configure mode
        conn.execute("configure")

# configure static route
        for i in data['config']:
            conn.execute(basic_configuration % (i['target'],
                                                i['next-hop'],
                                                i['distance']))

# commit configuration
        conn.execute("commit")

# save configuration
        conn.execute("save")

# exit configure mode
        conn.execute("exit")

# close connection
        conn.close(force=True)

        return {"Result": "Configured successfully"}

    except Exception, e:
        return {'Error': e}























