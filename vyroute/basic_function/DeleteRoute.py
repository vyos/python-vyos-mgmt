# author=hochikong
from Exscript.protocols import SSH2
from Exscript import Account


def deleteroute(data):
    """This method provide a router configuration delete function

    Parameter data example:
    {'router':'vyos@172.16.77.188','passwd':'vyos',
    'config':'rip'
    }

    WARNING!
    When you use this function,please don't forget this func will delete all same type
    router configuration,when your 'config' in data is 'rip',it will delete all rip router setting.
    If you do not want your setting disappear,you can delete router configuration manually or rewrite
    this func.

    :param data: a python dictionary
    :return: a python dictionary
    """
    delete_basic_configuration = "delete protocols %s"

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

        # delete specific configuration
        conn.execute(delete_basic_configuration % data['config'])

        # commit configuration
        conn.execute("commit")

        # save configuration
        conn.execute("save")

        # exit configure mode
        conn.execute("exit")

        # close connection
        conn.close(force=True)

        return {"Result": "Delete successfully"}

    except Exception, e:
        return {"Error": e}