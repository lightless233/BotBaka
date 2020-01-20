#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.pipeline.repeat_checker
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import random

from BotBaka.pipeline.base import BasePipeline
from BotBaka.utils.log import logger

last_message = ""
repeat_count = 0


class RepeatCheckerPipeline(BasePipeline):

    def __init__(self):
        super(RepeatCheckerPipeline, self).__init__()

        self.name = "RepeatCheckerPipeline"

    def process(self, from_group: int, from_qq: int, name: str, message: str) -> bool:

        global last_message, repeat_count

        if message == last_message:
            # 是复读的消息，累加计数
            repeat_count += 1
        else:
            # 不是复读的消息，更新计数
            last_message = message
            repeat_count = 1

        logger.debug("last_message: {}, count: {}".format(last_message, repeat_count))

        # 根据复读次数，进行概率ban
        # 1次、2次 不禁言
        # 10次以上 100%禁言
        if repeat_count in (1, 2):
            return True

        if repeat_count >= 10:
            self.CQApi.set_group_ban(from_group, from_qq, 10)
            self.CQApi.send_group_message(from_group, from_qq, "您怕不是个复读机吧？\n劝你次根香蕉冷静冷静!")
            return False

        # r = 1- (n-1)/n
        # n = 3 => r = 1/3
        # n = 4 => r = 1/4
        # n = 5 => r = 1/5
        # n = 6 => r = 1/6
        # ...
        # n = 9 => r = 1/9
        # 1 / (12 - n)
        prob = 2.0 / (11 - repeat_count)
        point = random.random()
        logger.info(f"prob: {prob}, point: {point}")
        if point < prob:
            self.CQApi.set_group_ban(from_group, from_qq, repeat_count * repeat_count / 2)
            self.CQApi.send_group_message(from_group, from_qq, "嘤嘤嘤，复读被抓住了呢!")
            return False

        return True
