# Copyright (c) 2016 Hochikong

from setuptools import setup, find_packages
setup(
    name="vymgmt",
    version="0.1",
    packages=find_packages(),
    install_requires=['pexpect'],

    description="A library for VyOS configurations",
    long_description="A library for VyOS configurations",
    author="Hochikong",
    author_email="hochikong@foxmail.com",

    license="MIT",
    keywords="A library for VyOS configurations",
    url="https://github.com/vyos/python-vyos-mgmt"
)
