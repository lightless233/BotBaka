#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.timer.engine.thread
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    基于线程的engine基类

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

# from __future__ import annotations

import abc
import multiprocessing
import threading
import typing

from .base import CommonBaseEngine


class SingleThreadEngine(CommonBaseEngine):
    """
    基于单线程的引擎模块
    """

    def __init__(self, name=None):
        super(SingleThreadEngine, self).__init__()
        self.name = name if name else "SingleThreadEngine"

    def start(self):
        self.status = self.EngineStatus.RUNNING
        self.thread: threading.Thread = threading.Thread(target=self._worker, name=self.name)
        self.thread.start()

    def stop(self, force=True):
        self.status = self.EngineStatus.STOP
        self.ev.set()

    def is_alive(self):
        return self.thread.is_alive()

    @abc.abstractmethod
    def _worker(self):
        pass


class MultiThreadEngine(CommonBaseEngine):
    """
    基于多线程的基础引擎
    """

    def __init__(self, name=None, pool_size=None):
        super(MultiThreadEngine, self).__init__()
        self.name = name if name else "MultiThreadEngine"
        self.pool_size = pool_size if pool_size else multiprocessing.cpu_count() * 2 + 1

    def start(self):
        self.status = self.EngineStatus.RUNNING
        self.thread_pool: typing.List[threading.Thread] = \
            [threading.Thread(
                target=self._worker, name="{}-{}".format(self.name, idx)
            ) for idx in range(self.pool_size)]
        _ = [t.start() for t in self.thread_pool]

    def stop(self, force=True):
        self.status = self.EngineStatus.STOP
        self.ev.set()

    def is_alive(self):
        return any([t.is_alive() for t in self.thread_pool])

    @abc.abstractmethod
    def _worker(self):
        pass
