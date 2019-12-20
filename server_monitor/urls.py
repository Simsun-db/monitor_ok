#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/18 10:56
# @Author  : SimSun
# @File    : urls.py
from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.login, name="login"),
  ]
