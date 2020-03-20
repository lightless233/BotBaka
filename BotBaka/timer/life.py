#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.timer.life
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


class LifeTimer(SingleThreadEngine):

    def __init__(self):
        super(LifeTimer, self).__init__()

        self.name = "life-timer"
        self.tag = f"[{self.name}]"
        self.target_group = 672534169

    def _worker(self):
        """
        每天早上9点30分，发送今年进度。
        """

        logger.debug(f"{self.tag} start!")

        while True:

            current_time = datetime.datetime.now()
            h = current_time.hour
            m = current_time.minute

            if h == 9 and m == 30:
                # 获取今天是今年的第几天
                today = datetime.date.today()
                deltas = today - datetime.date(today.year - 1, 12, 31)
                total_days = deltas.days

                # 先不管闰年，懒得算，等一个PR
                percent = round(total_days / 365 * 100, 2)

                message = "[虚度光阴小助手] \n今天是 {} 年的第 {} 天，今年已经过了 {}% 啦！".format(
                    today.year, total_days, percent
                )
                self.CQApi.send_group_message(group=self.target_group, qq=None, message=message, auto_at=False)

                self.ev.wait(65)

            self.ev.wait(60)
