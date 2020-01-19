#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.core.engine.base.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    BaseEngine

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import threading
from typing import List

import abc

from BotBaka.api import CQApi


class CommonBaseEngine(object):
    class EngineStatus:
        READY = 0x00
        RUNNING = 0x01
        STOP = 0x02

    def __init__(self):
        super(CommonBaseEngine, self).__init__()
        self.name = "BaseEngine"
        self.status = self.EngineStatus.READY
        self.ev: threading.Event = threading.Event()
        self.thread: threading.Thread = None
        self.thread_pool: List[threading.Thread] = None

        self.CQApi = CQApi()

    def is_running(self):
        return self.status == self.EngineStatus.RUNNING

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self, force=True):
        pass

    @abc.abstractmethod
    def is_alive(self):
        pass

    @abc.abstractmethod
    def _worker(self):
        pass
