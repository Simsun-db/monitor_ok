#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 10:27
# @Author  : SimSun
# @File    : dbtest.py
from tools import db_connect
from tools import config_manage
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'


# oracle eg.


def selectdata(dbname, vsql):
    con_dict = config_manage.read_byname(dbname)
    con = db_connect.conn_oracle(con_dict)
    cursor = con.cursor()
    cursor.execute(vsql)

    rows = []
    dictresult = {}
    columnNames = tuple([d[0] for d in cursor.description])
    for row in cursor.fetchall():
        # rows.append(dict(zip(columnNames, row)))
        rows.append(row)
        dictresult[columnNames] = rows
    cursor.close()
    con.close()
    return dictresult


vsql = "SELECT * FROM xt_sjdb_table_bz"
dictrows = selectdata('oracle46', vsql)
print(dictrows)

# mysql eg.
# con_dict=config_manage.read_byname('mysql25')
# con= db_connect.conn_mysql(con_dict)
# cursor=con.cursor()
#
# cursor.execute("""select * from users""")
# data=cursor.fetchone()
# print(data)
# cursor.close()
# con.close()
