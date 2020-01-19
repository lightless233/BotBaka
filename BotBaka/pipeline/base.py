#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.pipeline.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import abc

from BotBaka.api import CQApi


class BasePipeline:

    def __init__(self):
        super(BasePipeline, self).__init__()

        self.name = "default-pipeline"

        self.CQApi = CQApi()

    @abc.abstractmethod
    def process(self, from_group: int, from_qq: int, name: str, message: str) -> bool:
        """
        :param from_group:
        :param from_qq:
        :param name: 发送者的可读名称
        :param message:
        :return:
        """
        pass
