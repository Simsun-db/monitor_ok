#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 10:03
# @Author  : SimSun
# @File    : db_connect.py
import cx_Oracle
import MySQLdb


def conn_oracle(conn_dict):
    username = conn_dict['username']
    password = conn_dict['password']
    host = conn_dict['host']
    service_name = conn_dict['service_name']
    port = conn_dict['port']

    connect_str = username + '/' + password + \
        '@' + host + ':' + port + '/' + service_name
    con = cx_Oracle.Connection(connect_str)
    return con


def conn_mysql(conn_dict):
    username = conn_dict['username']
    password = conn_dict['password']
    host = conn_dict['host']
    service_name = conn_dict['service_name']
    port = int(conn_dict['port'])

    con = MySQLdb.connect(
        host=host,
        user=username,
        passwd=password,
        db=service_name,
        port=port)
    return con
