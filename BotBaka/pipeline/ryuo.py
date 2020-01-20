#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.pipeline.ryuo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from BotBaka.database.models import RyuoModel
from BotBaka.pipeline.base import BasePipeline


class RyuoPipeline(BasePipeline):

    def __init__(self):
        super(RyuoPipeline, self).__init__()

    def process(self, from_group: int, from_qq: int, name: str, message: str) -> bool:
        # 检查今天db里是否已经有这个人了
        # 如果没有，就加进去
        # 如果有，就计数+1

        if from_group != 672534169:
            # 只统计特定群的数据
            return True

        result: RyuoModel = RyuoModel.instance.get_today_user_by_qq(from_qq)
        if not result:
            RyuoModel.instance.create(qq=from_qq, cnt=1, nickname=name)
        else:
            result.cnt += 1
            result.nickname = name
            result.save()

        return True
