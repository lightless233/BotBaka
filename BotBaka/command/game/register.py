#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.game.register
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from typing import List

from BotBaka.command.base import BaseCommand
from BotBaka.database.models import PlayerModel


class RegisterSubCommand(BaseCommand):

    def __init__(self):
        super(RegisterSubCommand, self).__init__()

        self.command_name = "%game register"

        self.err_msg = "%game register"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        # %game register

        # 1 检查该QQ是否已经有角色了
        player_obj = PlayerModel.instance.get_player_by_qq(from_qq)
        if player_obj:
            self.CQApi.send_group_message(from_group, from_qq, "角色已存在。")
            return

        # 2 如果没有，就创建角色
        if PlayerModel.instance.create(qq=from_qq):
            self.CQApi.send_group_message(from_group, from_qq, "注册成功!")
        else:
            self.CQApi.send_group_message(from_group, from_qq, "注册失败!")
