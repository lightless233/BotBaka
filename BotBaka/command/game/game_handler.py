#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.game.game_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from typing import List

from ..base import BaseCommand
from .register import RegisterSubCommand
from .status import StatusSubCommand
from .pt import PtSubCommand


class GameCommand(BaseCommand):

    def __init__(self):
        super(GameCommand, self).__init__()

        self.command_name = "%game"

        self.sub_command = {
            "register": RegisterSubCommand(),
            "status": StatusSubCommand(),
            "pt": PtSubCommand(),
            "attack": None,
            "item": None,
            "skill": None,
        }

        self.error_message = """Unknown sub-command.
sub-command list:

%game register - 注册
%game status - 展示玩家资料
%game pt - 分配点数。格式：%game pt STR 1
%game attack - FIRE! FIRE! FIRE! 格式：%game attack @qq [skill_name]
"""

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        try:
            sub_command = command_list[1]
        except IndexError:
            self.CQApi.send_group_message(from_group, from_qq, self.error_message)
            return

        sub_command = sub_command.lower()
        if sub_command not in self.sub_command:
            self.CQApi.send_group_message(from_group, from_qq, self.error_message)
            return
        else:
            sub: BaseCommand = self.sub_command.get(sub_command)
            if sub is not None:
                sub.process(from_group, from_qq, name, command_list)
            else:
                self.CQApi.send_group_message(from_group, from_qq, self.error_message)
