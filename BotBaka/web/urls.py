#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.web.urls
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""

from django.urls import path

from .controller import event

urlpatterns = [
    path("event", event.EventView.as_view()),
]
