# Copyright (c) 2016 Hochikong

from setuptools import setup, find_packages
setup(
    name="vyroute",
    version="0.1",
    packages=find_packages(),
    install_requires=['pexpect'],

    description="A library for VyOS routing setting",
    long_description="A library for VyOS routing setting",
    author="Hochikong",
    author_email="michellehzg@gmail.com",

    license="MIT",
    keywords="A library for VyOS routing setting",
    url="https://github.com/vyos/python-vyos-mgmt"
)
