#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 8:15
# @Author  : SimSun
# @File    : config_manage.py
from configparser import ConfigParser
import os

fname = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)),
    'db_config.ini')


def read_byname(section_name):

    config = ConfigParser()
    config.read(fname, encoding='utf-8')
    ditems = {}
    if config.has_section(section_name):
        ditems = dict(config.items(section_name))
    else:
        ditems = None
    # print(ditems)
    return ditems


def read_all():
    config = ConfigParser()
    config.read(fname, encoding='utf-8')
    ditems = {}

    for sec in config.sections():
        ditems[sec] = dict(config.items(sec))
    # print(ditems)
    return ditems


read_all()
