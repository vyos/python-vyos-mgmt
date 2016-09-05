# Copyright (c) 2016 Hochikong


from pexpect import pxssh
from .mgmt_common import messenger, committer
from .base_exceptions.exceptions_for_set_and_delete import ConfigPathError, ConfigValueError
from .base_exceptions.exceptions_for_commit import CommitFailed, CommitConflict
from .base_exceptions.base import CommonError, MaintenanceError
from .error_distinguish import distinguish_for_set, distinguish_for_delete, distinguish_for_commit


class Router(object):
    def __init__(self, address, cred):
        """Initial a router object

        :param address: Router address,example:'192.168.10.10'
        :param cred: Router user and password,example:'vyos:vyos'
        """
        self.__address = address
        self.__cred = list(cred)
        self.__divi = self.__cred.index(":")
        self.__username = ''.join(self.__cred[:self.__divi])
        self.__passwd = ''.join(self.__cred[self.__divi+1:])
        self.__conn = pxssh.pxssh()
        self.__status = {"status": None, "commit": None, "save": None, "configure": None}
        self.__basic_string = {0: 'set ', 1: 'delete '}

    def status(self):
        """Check the router object inner status

        :return: A python dictionary include the status of the router object
        """
        return self.__status

    def login(self):
        """Login the router

        :return: A message or an error
        """
        has_error = None
        try:
            if self.__conn.login(self.__address, self.__username, self.__passwd) is True:
                self.__status["status"] = "login"
            else:
                has_error = 'Type1'
        except Exception as e:
            return e

        if has_error == 'Type1':
            raise MaintenanceError("Error : Connect Failed.")

    def logout(self):
        """Logout the router

        :return: A message or an error
        """
        has_error = None
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "No":
                    self.__conn.close()
                    self.__status["status"] = "logout"
                    self.__status["configure"] = None
                    self.__conn = pxssh.pxssh()
                elif self.__status["configure"] is None:
                    self.__conn.close()
                    self.__status["status"] = "logout"
                    self.__conn = pxssh.pxssh()
                else:
                    if self.__status["save"] == "Yes":
                        has_error = 'Type3'
                    elif self.__status["save"] is None:
                        has_error = 'Type3'
                    else:
                        if self.__status["commit"] == "Yes":
                            has_error = 'Type3'
                        elif self.__status["commit"] is None:
                            has_error = 'Type3'
                        else:
                            has_error = 'Type1'
            else:
                has_error = 'Type4'
        except Exception as e:
            return e

        if has_error == 'Type1':
            raise MaintenanceError("Error : You should commit and exit configure mode first.")
#        if has_error == 'Type2':
#            raise MaintenanceError("Error : You should save and exit configure mode first.")
        if has_error == 'Type3':
            raise MaintenanceError("Error : You should exit configure mode first.")
        if has_error == 'Type4':
            raise MaintenanceError("Error : Router object not connect to a router.")

    def configure(self):
        """Enter the VyOS configure mode

        :return: A message or an error
        """
        has_error = None
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] is not "Yes":
                    self.__conn.sendline("configure")
                    self.__conn.prompt(0)
                    self.__conn.set_unique_prompt()
                    self.__status["configure"] = "Yes"
                else:
                    has_error = 'Type1'
            else:
                has_error = 'Type2'
        except Exception as e:
            return e

        if has_error == 'Type1':
            raise MaintenanceError("Error : In configure mode now!")
        if has_error == 'Type2':
            raise MaintenanceError("Error : Router object not connect to a router.")

    def commit(self):
        """Commit the configuration changes

        :return: A message or an error
        """
        has_error = None
        result = None
        res = None
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    if self.__status["commit"] is None:
                        has_error = 'Type1'
                    if self.__status["commit"] == "No":
                        res = committer(self.__conn, "commit")
                        if "Result" in res:
                            self.__status["commit"] = "Yes"
                        else:
                            result = distinguish_for_commit(res)
                    else:
                        has_error = 'Type2'
                else:
                    has_error = 'Type3'
            else:
                has_error = 'Type4'
        except Exception as e:
            return e

        if has_error == 'Type1':
            raise MaintenanceError("Error : You don't need to commit.")
        if has_error == 'Type2':
            raise MaintenanceError("Error : You have commit!")
        if has_error == 'Type3':
            raise MaintenanceError("Error : Router not in configure mode!")
        if has_error == 'Type4':
            raise MaintenanceError("Error : Router object not connect to a router.")

        if result == "CommitFailed":
            raise CommitFailed(res)
        elif result == "CommitConflict":
            raise CommitConflict(res)

    def save(self):
        """Save the configuration after commit

        :return: A message or an error
        """
        has_error = None
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    if self.__status["commit"] == "Yes":
                        if self.__status["save"] is None:
                            has_error = 'Type1'
                        if self.__status["save"] == "No":
                            self.__conn.sendline("save")
                            self.__conn.prompt(0)
                            self.__status["save"] = "Yes"
                        else:
                            has_error = 'Type2'
                    elif self.__status["commit"] is None:
                        has_error = 'Type3'
                    else:
                        has_error = 'Type4'
                else:
                    has_error = 'Type5'
            else:
                has_error = 'Type6'
        except Exception as e:
            return e

        if has_error == 'Type1':
            raise MaintenanceError("Error : You don't need to save.")
        if has_error == 'Type2':
            raise MaintenanceError("Error : You have saved!")
        if has_error == 'Type3':
            raise MaintenanceError("Error : You don't need to save.")
        if has_error == 'Type4':
            raise MaintenanceError("Error : You need to commit first!")
        if has_error == 'Type5':
            raise MaintenanceError("Error : Router not in configure mode!")
        if has_error == 'Type6':
            raise MaintenanceError("Error : Router object not connect to a router.")

    def exit(self, force=False):
        """Exit VyOS configure mode

        :param force: True or False
        :return: A message or an error
        """
        has_error = None
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    if force is True:
                        self.__conn.sendline("exit discard")
                        self.__conn.prompt()
                        self.__status["configure"] = "No"
                        self.__status["save"] = None
                        self.__status["commit"] = None
                    else:
                        if self.__status["commit"] == "Yes":
                            if self.__status["save"] == "Yes":
                                self.__conn.sendline("exit")
                                self.__conn.prompt()
                                self.__status["configure"] = "No"
                                self.__status["save"] = None
                                self.__status["commit"] = None
                            elif self.__status["save"] == "No":
                                self.__conn.sendline("exit")
                                self.__conn.prompt()
                                self.__status["configure"] = "No"
                                self.__status["save"] = None
                                self.__status["commit"] = None
                        elif self.__status["commit"] is None:
                            self.__conn.sendline("exit")
                            self.__conn.prompt()
                            self.__status['configure'] = "No"
                        else:
                            has_error = 'Type2'
                else:
                    has_error = 'Type3'
            else:
                has_error = 'Type4'
        except Exception as e:
            return e

        if has_error == 'Type2':
            raise MaintenanceError("Error : You should commit first.")
        if has_error == 'Type3':
            raise MaintenanceError("Error : You are not in configure mode,no need to exit.")
        if has_error == 'Type4':
            raise MaintenanceError("Error : Router object not connect to a router.")

    def set(self, config):
        """Basic 'set' method,execute the set command in VyOS

        :param config: A configuration string.
                       e.g. 'protocols static route ... next-hop ... distance ...'
        :return: A message or an error
        """
        has_error = None
        result = None
        res = None
        full_config = self.__basic_string[0] + config
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = messenger(self.__conn, full_config)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                    else:
                        result = distinguish_for_set(res)
                else:
                    has_error = 'Type1'
            else:
                has_error = 'Type2'
        except Exception as e:
            return e

        if has_error == 'Type1':
            raise MaintenanceError("Error : You are not in configure mode.")
        if has_error == 'Type2':
            raise MaintenanceError("Error : Router object not connect to a router.")

        if result == "ConfigPathError":
            raise ConfigPathError(res)
        elif result == "ConfigValueError":
            raise ConfigValueError(res)
        elif result == "NonsupportButError":
            raise CommonError(res)

    def delete(self, config):
        """Basic 'delete' method,execute the delete command in VyOS

        :param config: A configuration string.
                               e.g. 'protocols static route ... next-hop ... distance ...'
        :return: A message or an error
        """
        has_error = None
        result = None
        res = None
        full_config = self.__basic_string[1] + config
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = messenger(self.__conn, full_config)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                    else:
                        result = distinguish_for_delete(res)
                else:
                    has_error = 'Type1'
            else:
                has_error = 'Type2'
        except Exception as e:
            return e

        if has_error == 'Type1':
            raise MaintenanceError("Error : You are not in configure mode.")
        if has_error == 'Type2':
            raise MaintenanceError("Error : Router object not connect to a router.")

        if result == "ConfigPathError":
            raise ConfigPathError(res)
        elif result == "ConfigValueError":
            raise ConfigValueError(res)
        elif result == "NonsupportButError":
            raise CommonError(res)
