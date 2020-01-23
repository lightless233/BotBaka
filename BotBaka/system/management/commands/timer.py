#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.system.management.commands.timer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    启动timer

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import signal

from django.core.management import BaseCommand

from BotBaka.timer import SecNewsTimer, RyuoTimer, InviteTimer, RSSTimer
from BotBaka.utils.log import logger


class Command(BaseCommand):
    help = "Start timer."

    def __init__(self):
        super(Command, self).__init__()

        self.timers = [
            SecNewsTimer(),
            RyuoTimer(),
            InviteTimer(),
            RSSTimer(),
        ]

    def __sigint_handler(self, sig, frame):
        logger.info("Receive exit signal.")
        for t in self.timers:
            t.stop()

    def handle(self, *args, **options):

        # 注册 CTRL+C 信号，不然 timer 无法正常退出

        signal.signal(signal.SIGINT, self.__sigint_handler)

        for timer in self.timers:
            timer.start()
