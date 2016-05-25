# author=hochikong
from Exscript.protocols import SSH2
from Exscript import Account
from vyroute.basic_function import Modifylo
from vyroute.basic_function import StaticRoute
from vyroute.basic_function import RIPRoute
from vyroute.basic_function import OSPFRoute


class Router(object):
    # Static router configuration func
    def static_route(self, data):
        pass

    # RIP router configuration func
    def rip_route(self, data):
        pass

    # OSPF router configuration func
    def ospf_area(self, data):
        pass

    def router_id(self, data):
        pass

    def ospf_redistribute(self, data):
        pass

    def ospf_adjacency(self):
        pass

    def ospf_default_route(self, data):
        pass

    def ospf_route_map(self, data):
        pass

    # Interfaces configuration func
    def lo(self, data):
        pass

    def delete_route(self, data):
        pass

    # Basic VyOS configuration func
    def configure(self):
        pass

    def commit_config(self):
        pass

    def save_config(self):
        pass

    def exit_config(self):
        pass

    # Login and logout a router
    def login(self):
        pass

    def logout(self):
        pass


class BasicRouter(Router):
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
        self.__account = Account(self.__username, self.__passwd)
        self.__conn = SSH2()
        self.status = {"object": None, "commit": None, "save": None, "configure": None}

    def login(self):
        """Login the router

        :return: a python dictionary
        """
        try:
            if self.__conn.connect(self.__address) is True:
                self.__conn.login(self.__account)
                self.status["object"] = "login"
                return {"Result": "Login successfully."}
            else:
                return {"Error": "Connect Failed."}
        except Exception, e:
            return {"Error": e}

    def logout(self):
        """Logout the router

        :return: a python dictionary
        """
        try:
            self.__conn.close(force=True)
            self.status["object"] = "logout"
            return {"Result": "Logout successfully."}
        except Exception, e:
            return {"Error": e}

    def configure(self):
        """Enter the VyOS configure mode

        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] is None:
                    self.__conn.execute("configure")
                    self.status["configure"] = "Yes"
                    return {"Result": "Active configure mode successfully."}
                else:
                    return {"Error": "In configure mode now!"}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def commit_config(self):
        """Commit the configuration changes

        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    if self.status["commit"] is None:
                        return {"Error": "You don't need to commit."}
                    if self.status["commit"] == "No":
                        self.__conn.execute("commit")
                        self.status["commit"] = "Yes"
                        return {"Result": "Commit successfully."}
                    else:
                        return {"Error": "You have committed!"}
                else:
                    return {"Error": "Router not in configure mode!"}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def save_config(self):
        """Save the configuration after commit

        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    if self.status["commit"] == "Yes":
                        if self.status["save"] is None:
                            return {"Error": "You don't need to save."}
                        if self.status["save"] == "No":
                            self.__conn.execute("save")
                            self.status["save"] = "Yes"
                            return {"Result": "Save successfully."}
                        else:
                            return {"Error": "You have saved!"}
                    else:
                        return {"Error": "You need to commit first!"}
                else:
                    return {"Error": "Router not in configure mode!"}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def exit_config(self, force=False):
        """Exit VyOS configure mode

        :param force: True or False
        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    if force is True:
                        self.__conn.execute("exit")
                        self.status["configure"] = None
                        self.status["save"] = None
                        self.status["commit"] = None
                        return {"Result": "Exit configure mode successfully."}
                    if force is False:
                        if self.status["commit"] == "Yes":
                            if self.status["save"] == "Yes":
                                self.__conn.execute("exit")
                                self.status["configure"] = None
                                self.status["save"] = None
                                self.status["commit"] = None
                                return {"Result": "Exit configure mode successfully."}
                            else:
                                return {"Error": "You should save first."}
                        else:
                            return {"Error": "You should commit first."}
                else:
                    return {"Error": "You are not in configure mode,need not exit."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def lo(self, data):
        """Modify a router loopback address

        :param data: a python dictionary
        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    res = Modifylo.modifylo(self.__conn, data)
                    if "Result" in res:
                        if self.status["commit"] == "No":
                            pass
                        else:
                            self.status["commit"] = "No"
                        if self.status["save"] == "No":
                            pass
                        else:
                            self.status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return {"Error": "You are not in configure mode."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def static_route(self, data):
        """Static router setting

        Parameter data example:
        {'config':{'target':'10.20.10.0/24','next-hop':'10.20.10.1','distance':'1'},
        }

        :param data: a python dictionary
        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    res = StaticRoute.staticroute(self.__conn, data)
                    if "Result" in res:
                        if self.status["commit"] == "No":
                            pass
                        else:
                            self.status["commit"] = "No"
                        if self.status["save"] == "No":
                            pass
                        else:
                            self.status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return {"Error": "You are not in configure mode."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def rip_route(self, data):
        """RIP protocols router setting

        Parameter data example:
        {'config':'192.168.10.0/24',
        }

        :param data: a python dictionary
        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    res = RIPRoute.riproute(self.__conn, data)
                    if "Result" in res:
                        if self.status["commit"] == "No":
                            pass
                        else:
                            self.status["commit"] = "No"
                        if self.status["save"] == "No":
                            pass
                        else:
                            self.status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return {"Error": "You are not in configure mode."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def ospf_area(self, data):
        """OSPF area setting

         Parameter data example:
         {'config':{'area':'0','network':'192.168.10.0/24'},
         }

        :param data: a python dictionary
        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    res = OSPFRoute.ospfarea(self.__conn, data)
                    if "Result" in res:
                        if self.status["commit"] == "No":
                            pass
                        else:
                            self.status["commit"] = "No"
                        if self.status["save"] == "No":
                            pass
                        else:
                            self.status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return {"Error": "You are not in configure mode."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def router_id(self, data):
        """OSPF router id setting

        Parameter data example:
        {'config':{'id':'1.1.1.1'},
        }

        :param data: a python dictionary
        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    res = OSPFRoute.router_id(self.__conn, data)
                    if "Result" in res:
                        if self.status["commit"] == "No":
                            pass
                        else:
                            self.status["commit"] = "No"
                        if self.status["save"] == "No":
                            pass
                        else:
                            self.status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return {"Error": "You are not in configure mode."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def ospf_redistribute(self, data):
        """OSPF redistribute setting

        Parameter data example:
        {'config':{'type':'2'},
        }

        :param data: a python dictionary
        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    res = OSPFRoute.ospf_redistribute(self.__conn, data)
                    if "Result" in res:
                        if self.status["commit"] == "No":
                            pass
                        else:
                            self.status["commit"] = "No"
                        if self.status["save"] == "No":
                            pass
                        else:
                            self.status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return {"Error": "You are not in configure mode."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def ospf_adjacency(self):
        """set protocols ospf log-adjacency-changes

        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    res = OSPFRoute.ospf_adjacency(self.__conn)
                    if "Result" in res:
                        if self.status["commit"] == "No":
                            pass
                        else:
                            self.status["commit"] = "No"
                        if self.status["save"] == "No":
                            pass
                        else:
                            self.status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return {"Error": "You are not in configure mode."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def ospf_default_route(self, data):
        """set protocols ospf default-information originate always (and other 2 commands)

        Parameter data example:
        {'config':{'metric':'10','metric-type':'2'},
        }

        :param data: a python dictionary
        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    res = OSPFRoute.ospf_default_route(self.__conn, data)
                    if "Result" in res:
                        if self.status["commit"] == "No":
                            pass
                        else:
                            self.status["commit"] = "No"
                        if self.status["save"] == "No":
                            pass
                        else:
                            self.status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return {"Error": "You are not in configure mode."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}

    def ospf_route_map(self, data):
        """VyOS route-map setting when you configure a OSPF router

        Parameter data example:
        {'config':{'rule':'10','interface':'lo'},
        }

        :param data: a python dictionary
        :return: a python dictionary
        """
        try:
            if self.status["object"] == "login":
                if self.status["configure"] == "Yes":
                    res = OSPFRoute.ospf_route_map(self.__conn, data)
                    if "Result" in res:
                        if self.status["commit"] == "No":
                            pass
                        else:
                            self.status["commit"] = "No"
                        if self.status["save"] == "No":
                            pass
                        else:
                            self.status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return {"Error": "You are not in configure mode."}
            else:
                return {"Error": "Router object not connect to a router."}
        except Exception, e:
            return {"Error": e}