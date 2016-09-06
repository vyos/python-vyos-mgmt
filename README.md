VyMGMT
======

A python library for executing commands on VyOS systems.

Generic methods should also work with any of the Vyatta descendants (EdgeOS, Brocade vRouter).

The library is compatible with both python2 and python3.

It is released under the MIT license.

## How it works

VyMGMT uses pexpect.pxssh library to login to VyOS and execute commands there. This approach has
its downsides, but it's better than nothing.

Why is it better than using pxssh or another expect library directly?
To make life easier for the user, it provides methods such as set(), delete(), and commit()
that detect errors and raise appropriate exceptions when an error occurs.

## API reference

Will be on readthedocs soon.

## Installation

Will be on PyPI soon.

## Usage example

```
import vymgmt

vyos = vymgmt.Router('10.217.16.15', 'vyos', password='vyos', port=22)

vyos.login()
vyos.configure()

vyos.set("protocols static route 203.0.113.0/25 next-hop 192.0.2.20")
vyos.delete("system options reboot-on-panic")

vyos.commit()
vyos.save()
vyos.exit()
vyos.logout()

```

If something goes wrong, an exception is raised and the original error message from VyOS is included in its error string:

```
>>> vyos.set("system foobar true")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File ".../vymgmt/router.py", line 216, in set
    raise ConfigError(output)
vymgmt.router.ConfigError:  set system foobar true

  Configuration path: system [foobar] is not valid
  Set failed

[edit]

```

If you want to execute a command that is not yet supported explicitly, you can use run_op_mode_command() and
run_conf_mode_command() methods that take a full command and execute it on the other side.

## Behaviour

All methods raise a VyOSError exception if you try to use them when the Router object is in a wrong state,
such as trying to run configure() before logging in, or trying to run set() before configure().

If something goes wrong on the other side, ConfigError or its subclass CommitError is raised.
One special case, ConfigLocked (a subclass of CommitError) is raised when commit fails because there
is another commit in progress. It's made a special case because it's the only commit error that can
be recovered from easily (just wait a bit and retry).

By default, exit() will not let you exit and will raise a VyOSError is there are uncommited or unsaved changes.
You can override it with exit(force=True).

## Credits

This library was originally written by Hochikong (hochikong@foxmail.com (preferred), or michellehzg@gmail.com),
and is now maintained by the VyOS project.
