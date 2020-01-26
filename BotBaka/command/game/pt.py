#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.game.pt
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from typing import List

from django.db.models import F

from BotBaka.command.base import BaseCommand
from BotBaka.database.models import PlayerModel


class PtSubCommand(BaseCommand):
    def __init__(self):
        super(PtSubCommand, self).__init__()

        self.command_name = "%game pt"

        self.err_msg = "%game pt STR 2"

        self.available_prop = ["STR", "VIT", "AGI"]

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        """
        点数分配
        :param from_group:
        :param from_qq:
        :param name:
        :param command_list:
        """

        # 获取参数
        try:
            prop = command_list[2]
            pt = int(command_list[3])
        except (IndexError, ValueError):
            self.CQApi.send_group_message(from_group, from_qq, "格式错误，{}".format(self.err_msg))
            return

        prop = prop.upper()
        if prop not in self.available_prop:
            self.CQApi.send_group_message(from_group, from_qq, "格式错误，{}".format(self.err_msg))
            return

        # 获取这个玩家的所有剩余PT
        pc: PlayerModel = PlayerModel.instance.get_player_by_qq(from_qq)
        if pc is None:
            self.CQApi.send_group_message(from_group, from_qq, "请先注册后再进行游戏!")
            return
        player_rest_pt = pc.rest_pt
        if pt < 0 or pt > player_rest_pt:
            self.CQApi.send_group_message(from_group, from_qq, "PT不足!")
            return

        """
        更新PT，要一起更新其他数值
        """
        if PlayerModel.instance.update_player_prop(from_qq, prop, pt):
            self.CQApi.send_group_message(from_group, from_qq, "加点成功!")
        else:
            self.CQApi.send_group_message(from_group, from_qq, "加点失败!")
