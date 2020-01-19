#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.pipeline.thumb_checker
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""

from .base import BasePipeline


class ThumbCheckerPipeline(BasePipeline):

    def __init__(self):
        super(ThumbCheckerPipeline, self).__init__()

        self.name = "ThumbCheckerPipeline"

        self.blacklist = [
            "&#91;强&#93;",
            "[CQ:face,id=76]",
            b"\xf0\x9f\x91\x8d".decode("UTF-8"),
            "[CQ:emoji,id=128077]",
            "4",

        ]

    def process(self, from_group: int, from_qq: int, name: str, message: str) -> bool:

        thumb_cnt = 0

        for black_char in self.blacklist:
            if black_char in message:
                thumb_cnt += message.count(black_char)
                break

        if thumb_cnt > 0:
            self.CQApi.set_group_ban(from_group, from_qq, 2 * thumb_cnt)
            self.CQApi.send_group_message(from_group, from_qq, "嘤嘤嘤，发现大拇指了呢，呐，大拇指什么的是不可以的呢！")
            return False

        return True
