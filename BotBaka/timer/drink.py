#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.timer.drink
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import datetime

from .engine.thread import SingleThreadEngine
from ..utils.log import logger


class DrinkTimer(SingleThreadEngine):

    def __init__(self):
        super(DrinkTimer, self).__init__()

        self.name = "drink-timer"
        self.tag = f"[{self.name}]"
        self.target_group = 672534169

    def _worker(self):
        """
        从早上10点开始，到下午6点，每隔一个小时提醒一次
        改成2小时一次，并且周末不提醒
        """

        logger.debug(f"{self.tag} start!")

        while self.is_running():

            current_time = datetime.datetime.now()
            h = current_time.hour
            m = current_time.minute

            # 周末不提醒
            if current_time.weekday() in (5, 6):
                self.ev.wait(60)
                continue

            # 10 ~ 18
            if h < 10 or h > 18:
                self.ev.wait(60)
                continue

            # 13点不发，午休
            if h == 13:
                self.ev.wait(65)
                continue

            if m == 0:
                # 整点了，该发消息了
                if h == 18:
                    message = "【喝水提醒小助手】\n该喝水了哦~\n晚上也要多~喝~水~哦~"
                elif h % 2 == 0:
                    message = "【喝水提醒小助手】\n该喝水了哦~"

                self.CQApi.send_group_message(group=self.target_group, qq=None, message=message, auto_at=False)
                self.ev.wait(65)    # 比1分钟多sleep一会，保证同一分钟不会发两次消息

            self.ev.wait(60)
