#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.timer.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""

import abc

from BotBaka.api import CQApi


class BaseTimer:

    def __init__(self):
        super(BaseTimer, self).__init__()

        self.CQApi = CQApi()

        self.name = "base-timer"

    @abc.abstractmethod
    def process(self):
        pass
