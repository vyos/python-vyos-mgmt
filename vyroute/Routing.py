# author=hochikong
import StaticRoute


class BasicRouting(object):
    def static_routing(self):
        pass

    def rip_routing(self):
        pass

    def ospf_routing(self):
        pass


class Routing(BasicRouting):
    def __init__(self, datafile):
        """Initial member self.file.

        :param datafile: a string
        """
        self.file = datafile

    def static_routing(self, data):
        return StaticRoute.staticroute(data)





