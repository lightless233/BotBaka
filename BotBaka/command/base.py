#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.base
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import abc
from typing import List

from django.conf import settings

from BotBaka.api import CQApi


class BaseCommand:
    def __init__(self):
        super(BaseCommand, self).__init__()

        self.command_name = "%default"

        self.from_group: int = 0
        self.from_qq: int = 0

        self.CQApi = CQApi()

    def _check_admin(self, from_group, from_qq) -> bool:
        if from_qq not in settings.ADMIN_QQ:
            self.CQApi.send_group_message(from_group, from_qq, "你还不是管理员呢！不能使用这样的命令哦！")
            self.CQApi.set_group_ban(from_group, from_qq, 1)
            return False
        else:
            return True

    @abc.abstractmethod
    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        pass
