# author=hochikong
from Exscript.protocols import SSH2
from Exscript import Account


def riproute(data):
    """This method provide a RIP protocols router configuration function

    Parameter data example:
    {'router':'vyos@172.16.77.188','passwd':'vyos',
    'config':['192.168.10.0/24','10.20.10.0/24'],
    }

    :param data: a python dictionary
    :return: a python dictionary
    """
    rip_basic_configuration = "set protocols rip network %s"
    redistribute_configuration = "set protocols rip redistribute connected"
    try:
        stringlist = list(data['router'])
        divi = stringlist.index('@')
        user = ''.join(stringlist[:divi])
        passwd = data['passwd']
        address = ''.join(stringlist[divi + 1:])
        account = Account(user, passwd)
        conn = SSH2()
        conn.connect(address)
        conn.login(account)

        # configure mode
        conn.execute("configure")

        # configure RIP router
        for i in data['config']:
            conn.execute(rip_basic_configuration % i)

        conn.execute(redistribute_configuration)

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
        return {"Error": e}

