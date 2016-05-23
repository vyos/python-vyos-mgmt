# author=hochikong
from Exscript.protocols import SSH2
from Exscript import Account


def modifylo(data):
    """This method provide a loopback address configuration function

    Parameter data example:
    {'router':'vyos@172.16.77.188','passwd':'vyos','config':'1.1.1.1/32'
    }

    :param data: a python dictionary
    :return: a python dictionary
    """
    lo_basic_configuration = "set interfaces loopback lo address %s"

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

# configure loopback interface lo address
        conn.execute(lo_basic_configuration % data['config'])

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
