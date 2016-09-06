.. VyMGMT documentation master file, created by
   sphinx-quickstart on Tue Sep  6 14:12:19 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to VyMGMT's documentation!
==================================

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Quick introduction
==================

A python library for executing commands on VyOS systems.

Generic methods should also work with any of the Vyatta descendants (EdgeOS, Brocade vRouter).

The library is compatible with both python2 and python3.

It is released under the MIT license.

Usage example::

    import vymgmt

    vyos = vymgmt.Router('192.0.2.1', 'vyos', password='vyos', port=22)

    vyos.login()
    vyos.configure()

    vyos.set("protocols static route 203.0.113.0/25 next-hop 192.0.2.20")
    vyos.delete("system options reboot-on-panic")

    vyos.commit()
    vyos.save()
    vyos.exit()
    vyos.logout()
