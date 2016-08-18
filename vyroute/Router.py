# Copyright (c) 2016 Hochikong

from pxssh import pxssh
from vyroute.basic_function import Modifylo
from vyroute.basic_function import StaticRoute
from vyroute.basic_function import RIPRoute
from vyroute.basic_function import OSPFRoute
from vyroute.basic_function import DeleteRoute
from vyroute.basic_function import BGPRoute


class Router(object):
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
        self.__conn = pxssh()
        self.__status = {"status": None, "commit": None, "save": None, "configure": None}

    def status(self):
        """Check the router object inner status

        :return: A python dictionary include the status of the router object
        """
        return self.__status

    def login(self):
        """Login the router

        :return: A message or an error
        """
        try:
            if self.__conn.login(self.__address, self.__username, self.__passwd) is True:
                self.__status["status"] = "login"
                return "Result : Login successfully."
            else:
                return "Error : Connect Failed."
        except Exception as e:
            return e

    def logout(self):
        """Logout the router

        :return: A message or an error
        """
        try:
            self.__conn.close()
            self.__status["status"] = "logout"
            self.__status["configure"] = None
            self.__conn = pxssh()
            return "Result : Logout successfully."
        except Exception as e:
            return e

    def configure(self):
        """Enter the VyOS configure mode

        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] is not "Yes":
                    self.__conn.sendline("configure")
                    self.__conn.prompt(0)
                    self.__conn.set_unique_prompt()
                    self.__status["configure"] = "Yes"
                    return "Result : Active configure mode successfully."
                else:
                    return "Error : In configure mode now!"
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def commit(self):
        """Commit the configuration changes

        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    if self.__status["commit"] is None:
                        return "Error : You don't need to commit."
                    if self.__status["commit"] == "No":
                        self.__conn.sendline("commit")
                        self.__conn.prompt()
                        self.__status["commit"] = "Yes"
                        return "Result : Commit successfully."
                    else:
                        return "Error : You have committed!"
                else:
                    return "Error : Router not in configure mode!"
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def save(self):
        """Save the configuration after commit

        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    if self.__status["commit"] == "Yes":
                        if self.__status["save"] is None:
                            return "Error : You don't need to save."
                        if self.__status["save"] == "No":
                            self.__conn.sendline("save")
                            self.__conn.prompt(0)
                            self.__status["save"] = "Yes"
                            return "Result : Save successfully."
                        else:
                            return "Error : You have saved!"
                    elif self.__status["commit"] is None:
                        return "Error : You don't need to save."
                    else:
                        return "Error : You need to commit first!"
                else:
                    return "Error : Router not in configure mode!"
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def exit(self, force=False):
        """Exit VyOS configure mode

        :param force: True or False
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    if force is True:
                        self.__conn.sendline("exit discard")
                        self.__conn.prompt()
                        self.__status["configure"] = "No"
                        self.__status["save"] = None
                        self.__status["commit"] = None
                        return "Result : Exit configure mode successfully."
                    else:
                        if self.__status["commit"] == "Yes":
                            if self.__status["save"] == "Yes":
                                self.__conn.sendline("exit")
                                self.__conn.prompt()
                                self.__status["configure"] = "No"
                                self.__status["save"] = None
                                self.__status["commit"] = None
                                return "Result : Exit configure mode successfully."
                            else:
                                return "Error : You should save first."
                        elif self.__status["commit"] is None:
                            self.__conn.sendline("exit")
                            self.__conn.prompt()
                            self.__status['configure'] = "No"
                            return "Result : Exit configure mode successfully."
                        else:
                            return "Error : You should commit first."
                else:
                    return "Error : You are not in configure mode,need not exit."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def lo(self, lo_address):
        """Add a router loopback address

        Parameter example:
        '1.1.1.1/32'

        :param lo_address: The target address you want.Don't forget the netmask
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = Modifylo.modifylo(self.__conn, lo_address)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def delete_route(self, route_type):
        """Delete router configurations

        Parameter example:
        'rip'/'static'/'ospf'/'bgp'/'all'

        WARNING!
        When you use this function,please don't forget this func will delete all same type
        router configuration,when your 'config' in data is 'rip',it will delete all rip router setting.
        If you do not want your setting disappear,you can delete router configuration manually or rewrite
        this func.

        :param route_type: Route type
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = DeleteRoute.deleteroute(self.__conn, route_type)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def static_route(self, network_range, next_hop, distance):
        """This method provide a basic static router configuration function

        Parameter example:
        'network_range':'10.20.10.0/24'
        'next-hop':'10.20.10.1'
        'distance':'1'

        :param network_range: The target network,don't forget the netmask
        :param next_hop: The next hop
        :param distance: The distance
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = StaticRoute.staticroute(self.__conn, network_range, next_hop, distance)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def rip_network(self, network_range):
        """RIP router network setting

        Parameter example:
        '10.20.10.0/24'

        :param network_range: The target network,don't forget the netmask
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = RIPRoute.rip_network(self.__conn, network_range)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def rip_redistribute(self):
        """Execute 'set protocols rip redistribute connected' command

        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = RIPRoute.rip_redistribute(self.__conn)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def ospf_area(self, area, network_range):
        """This method provide a OSPF area configuration function

        Parameter example:
        'area':'0'
        'network_range':'192.168.10.0/24'

        :param area: The ospf area number
        :param network_range: The target network,don't forget the netmask
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = OSPFRoute.ospfarea(self.__conn, area, network_range)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def ospf_router_id(self, router_id):
        """This method provide a router id configuration function

        Parameter example:
        '1.1.1.1'

        :param router_id: The router id
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = OSPFRoute.ospf_router_id(self.__conn, router_id)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def ospf_redistribute(self, metric_type):
        """OSPF redistribute setting

        Parameter example:
        '2'

        :param metric_type: The metric-type
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = OSPFRoute.ospf_redistribute(self.__conn, metric_type)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def ospf_adjacency(self):
        """Execute 'Set protocols ospf log-adjacency-changes' command

        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = OSPFRoute.ospf_adjacency(self.__conn)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def ospf_default_route(self, metric, metric_type):
        """This method execute the commands to configure default route

        Parameter example:
        'metric':'10'
        'metric-type':'2'

        :param metric: The metric,a number
        :param metric_type: The metric-type
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = OSPFRoute.ospf_default_route(self.__conn, metric, metric_type)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def ospf_route_map(self, rule, interface):
        """VyOS route-map setting when you configure a OSPF router

        Parameter example:
        'rule':'10'
        'interface':'lo'

        :param rule: The route-map rule number
        :param interface: The interface name
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = OSPFRoute.ospf_route_map(self.__conn, rule, interface)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def bgp_route(self, self_as, neighbor, multihop, remote_as, update_source):
        """VyOS BGP router basic setting

        Parameter example:
        'self_as':'65538'
        'neighbor':'192.168.10.5'
        'multihop':'2'
        'remote_as':'65537'
        'update_source':'192.168.10.6'

        :param self_as: The AS number of the router you login
        :param neighbor: The neighbor router address
        :param multihop: The amount of hops
        :param remote_as: The remote AS number
        :param update_source: The update source
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = BGPRoute.bgp_as(self.__conn, self_as, neighbor, multihop, remote_as, update_source)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def bgp_network(self, self_as, network_range):
        """Add a network to BGP router

        Parameter example:
        'self_as':'65538'
        'network_range':'10.20.10.0/24'

        :param self_as: The AS number of the router you login
        :param network_range: The target network,don't forget the netmask
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = BGPRoute.bgp_network(self.__conn, self_as, network_range)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def bgp_router_id(self, self_as, router_id):
        """Set a router id for the router you login

        Parameter example:
        'self_as':'65538'
        'router_id':'10.20.10.0'

        :param self_as: The AS number of the router you login
        :param router_id: The router id,or you can use the router address as router id
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = BGPRoute.bgp_router_id(self.__conn, self_as, router_id)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e

    def bgp_blackhole_route(self, network_range):
        """Set a blackhole route

        Parameter example:
        '10.20.10.0/24'

        :param network_range: The target network,don't forget the netmask
        :return: A message or an error
        """
        try:
            if self.__status["status"] == "login":
                if self.__status["configure"] == "Yes":
                    res = BGPRoute.bgp_blackhole_route(self.__conn, network_range)
                    if "Result" in res:
                        if self.__status["commit"] == "No":
                            pass
                        else:
                            self.__status["commit"] = "No"
                        if self.__status["save"] == "No":
                            pass
                        else:
                            self.__status["save"] = "No"
                        return res
                    else:
                        return res
                else:
                    return "Error : You are not in configure mode."
            else:
                return "Error : Router object not connect to a router."
        except Exception as e:
            return e
