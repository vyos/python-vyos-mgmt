# Copyright (c) 2016 VyOS maintainers and contributors
# Portions copyright 2016 Hochikong
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""
.. module:: vymgmt
   :platform: Unix
   :synopsis: Provides a programmatic interface to VyOS router configuration sessions

.. moduleauthor:: VyOS Team <maintainers@vyos.net>, Hochikong


"""

import re

from pexpect import pxssh


class VyOSError(Exception):
    """ Raised on general errors """
    pass


class ConfigError(VyOSError):
    """ Raised when an error is found in configuration """
    pass


class CommitError(ConfigError):
    """ Raised on commit failures """
    pass


class ConfigLocked(CommitError):
    """ Raised when commit failes due to another commit in progress """
    pass


class Router(object):
    """ Router configuration interface class
    """
    def __init__(self, address, user, password='', port=22):
        """ Router configuration interface class

        :param address: Router address,example:'192.0.2.1'
        :param user: Router user
        :param password: Router user's password
        :param port: SSH port
        """
        self.__address = address
        self.__user = user
        self.__password = password
        self.__port = port

        # Session flags
        self.__logged_in = False
        self.__session_modified = False
        self.__session_saved = True
        self.__conf_mode = False

        # String codec, hardcoded for now
        self.__codec = "utf8"

    def __execute_command(self, command):
        """ Executed a command on the router

        :param command: The configuration command
        :returns: string -- Command output
        :raises: VyOSError
        """
        self.__conn.sendline(command)

        if not self.__conn.prompt():
            raise VyOSError("Connection timed out")

        output = self.__conn.before

        # XXX: In python3 it's bytes rather than str
        if isinstance(output, bytes):
            output = output.decode(self.__codec)
        return output

    def _status(self):
        """ Returns the router object status for debugging

        :returns: dict -- Router object status
        """
        return {"logged_in": self.__logged_in,
                "session_modified": self.__session_modified,
                "session_saved": self.__session_saved,
                "conf_mode": self.__conf_mode}

    def login(self):
        """ Logins to the router

        """

        # XXX: after logout, old pxssh instance stops working,
        # so we create a new one for each login
        # There may or may not be a better way to handle it
        self.__conn = pxssh.pxssh()

        self.__conn.login(self.__address, self.__user, password=self.__password, port=self.__port)
        self.__logged_in = True

    def logout(self):
        """ Logouts from the router

        :raises: VyOSError

        """

        if not self.__logged_in:
            raise VyOSError("Not logged in")
        else:
            if self.__conf_mode:
                raise VyOSError("Cannot logout before exiting configuration mode")
            else:
                self.__conn.close()
                self.__conn = None
                self.__logged_in = False

    def run_op_mode_command(self, command):
        """ Executes a VyOS operational command

        :param command: VyOS operational command
        :type command: str
        :returns: string -- Command output
        """

        prefix = ""
        # In cond mode, op mode commands require the "run" prefix
        if self.__conf_mode:
            prefix = "run"

        return self.__execute_command("{0} {1}".format(prefix, command))

    def run_conf_mode_command(self, command):
        """ Executes a VyOS configuration command

        :param command: VyOS configuration command
        :returns: Command output
        :raises: VyOSError
        """
        if not self.__conf_mode:
            raise VyOSError("Cannot execute configuration mode commands outside of configuration mode")
        else:
            return self.__execute_command(command)

    def configure(self):
        """ Enters configuration mode on the router

        You cannot use this methods before you log in.
        You cannot call this method twice, unless you log out and log back in.

        :raises: VyOSError
        """
        if not self.__logged_in:
            raise VyOSError("Cannot enter configuration mode when not logged in")
        else:
            if self.__conf_mode:
                raise VyOSError("Session is already in configuration mode")
            else:
                # configure changes the prompt (from $ to #), so this is
                # a bit of a special case, and we use pxssh directly instead
                # of the __execute_command wrapper...
                self.__conn.sendline("configure")

                # XXX: set_unique_prompt() after this breaks things, for some reason
                # We should find out why.
                self.__conn.PROMPT = "[#$]"

                if not self.__conn.prompt():
                    raise VyOSError("Entering configure mode failed (possibly due to timeout)")

                self.__conf_mode = True

                # XXX: There should be a check for operator vs. admin
                # mode and appropriate exception, but pexpect doesn't work
                # with operator's overly restricted shell...

    def commit(self):
        """Commits configuration changes

        You must call the configure() method before using this one.

        :raises: VyOSError, ConfigError, CommitError, ConfigLocked

        """
        if not self.__conf_mode:
            raise VyOSError("Cannot commit without entering configuration mode")
        else:
            if not self.__session_modified:
                raise ConfigError("No configuration changes to commit")
            else:
                output = self.__execute_command("commit")

                if re.search(r"Commit\s+failed", output):
                    raise CommitError(output)
                if re.search(r"another\s+commit\s+in\s+progress", output):
                    raise ConfigLocked("Configuration is locked due to another commit in progress")

                self.__session_modified = False
                self.__session_saved = False

    def save(self):
        """Saves the configuration after commit

        You must call the configure() method before using this one.
        You do not need to make any changes and commit then to use this method.
        You cannot save if there are uncommited changes.

        :raises: VyOSError
        """
        if not self.__conf_mode:
            raise VyOSError("Cannot save when not in configuration mode")
        elif self.__session_modified:
            raise VyOSError("Cannot save when there are uncommited changes")
        else:
            self.__execute_command("save")
            self.__session_saved = True

    def exit(self, force=False):
        """ Exits configuration mode on the router

        You must call the configure() method before using this one.

        Unless the force argument is True, it disallows exit when there are unsaved
        or uncommited changes. Any uncommited changes are discarded on forced exit.

        If the session is not in configuration mode, this method does nothing.

        :param force: Force exit despite uncommited or unsaved changes
        :type force: bool
        :raises: VyOSError
        """
        if not self.__conf_mode:
            pass
        else:
            # XXX: would be nice to simplify these conditionals
            if self.__session_modified:
                if not force:
                    raise VyOSError("Cannot exit a session with uncommited changes, use force flag to discard")
                else:
                    self.__execute_command("exit discard")
                    self.__conf_mode = False
                    return
            elif (not self.__session_saved) and (not force):
                raise VyOSError("Cannot exit a session with unsaved changes, use force flag to ignore")
            else:
                self.__execute_command("exit")
                self.__conf_mode = False

    def set(self, path):
        """ Creates a new configuration node on the router

        You must call the configure() method before using this one.

        :param path: Configuration node path.
                       e.g. 'protocols static route ... next-hop ... distance ...'
        :raises: ConfigError
        """
        if not self.__conf_mode:
            raise ConfigError("Cannot execute set commands when not in configuration mode")
        else:
            output = self.__execute_command("{0} {1}". format("set", path))
            if re.search(r"Set\s+failed", output):
                raise ConfigError(output)
            elif re.search(r"already exists", output):
                raise ConfigError("Configuration path already exists")
            self.__session_modified = True

    def delete(self, path):
        """ Deletes a node from configuration on the router

        You must call the configure() method before using this one.

        :param path: Configuration node path.
                               e.g. 'protocols static route ... next-hop ... distance ...'
        :raises: ConfigError
        """
        if not self.__conf_mode:
            raise ConfigError("Cannot execute delete commands when not in configuration mode")
        else:
            output = self.__execute_command("{0} {1}". format("delete", path))
            if re.search(r"Nothing\s+to\s+delete", output):
                raise ConfigError(output)
            self.__session_modified = True
