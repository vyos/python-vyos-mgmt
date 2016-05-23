# author=hochikong
from vyroute.basic_function import RIPRoute
from vyroute.basic_function import StaticRoute


class BasicRouting(object):
    def static_routing(self,data):
        pass

    def rip_routing(self,data):
        pass

    def ospf_routing(self,data):
        pass


class Routing(BasicRouting):
    def static_routing(self, data):
        return StaticRoute.staticroute(data)

    def rip_routing(self,data):
        return RIPRoute.riproute(data)







