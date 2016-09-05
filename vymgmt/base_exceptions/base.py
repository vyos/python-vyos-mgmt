# Copyright (c) 2016 Hochikong

prefix = "\r\n"


class Error(Exception):
    pass


class CommonError(Error):
    def __init__(self, message):
        self.error_message = message

    def __str__(self):
        return prefix + self.error_message


class MaintenanceError(Error):
    def __init__(self, message):
        self.error_message = message

    def __str__(self):
        return prefix + self.error_message
