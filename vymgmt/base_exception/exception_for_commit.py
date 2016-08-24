# Copyright (c) 2016 Hochikong

from .base import Error

prefix = "\r\n"


class CommitFailed(Error):
    def __init__(self, message):
        self.error_message = message

    def __str__(self):
        return prefix + self.error_message


class CommitConflict(Error):
    def __init__(self, message):
        self.error_message = message

    def __str__(self):
        return prefix + self.error_message
