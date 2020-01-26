#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.game.status
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
from BotBaka.utils.log import logger
from BotBaka.utils.quick_at import QuickAt


class StatusSubCommand(BaseCommand):

    def __init__(self):
        super(StatusSubCommand, self).__init__()

        self.command_name = "%game status"

        self.err_msg = "%game status [@qq]"

    @staticmethod
    def convert(n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        # 初始化数据
        target_qq = None

        try:
            target_qq = command_list[2]
            # 没异常，说明要查看其他人的数据
            target_qq = QuickAt.get_qq_from_at_msg(target_qq)
            if target_qq is None:
                return
        except IndexError:
            # 没有指定参数，查看自己的数据
            target_qq = from_qq

        # 打一下log
        logger.info(f"[{self.command_name}] target_qq:{target_qq}")

        # 开始查询数据
        player_obj: PlayerModel = PlayerModel.instance.get_player_by_qq(target_qq)
        if player_obj is None:
            # 查无此人
            self.CQApi.send_group_message(from_group, from_qq, "请确认目标是否正确，或请先执行%game register nickname进行注册！")
            return

        # 格式化数据
        data_msg = "【角色状态】\n"
        data_msg += "玩家: " + QuickAt.build_at_msg(target_qq) + "\n"
        data_msg += f"可用点数 (Rest PT): {player_obj.rest_pt}\n"
        data_msg += f"等级 (Level): {player_obj.level}\n" \
                    f"当前经验 (Exp): {player_obj.exp}\n" \
                    f"==========\n" \
                    f"力量 (STR): {player_obj.base_str}\n" \
                    f"体质 (VIT): {player_obj.base_vit}\n" \
                    f"敏捷 (AGI): {player_obj.base_agi}\n" \
                    f"幸运 (LUK): {player_obj.base_luk}\n" \
                    f"==========\n" \
                    f"生命值 (HP): {player_obj.current_hp} / {player_obj.max_hp}\n" \
                    f"能力值 (SP): {player_obj.current_sp} / {player_obj.max_sp}\n" \
                    f"攻击力 (ATK): {player_obj.atk}\n" \
                    f"防御力 (DEF): {player_obj.defend}\n" \
                    f"暴击 (CRI): {self.convert(player_obj.cri * 100, 2)}%\n" \
                    f"命中 (HIT): {self.convert(player_obj.hit * 100, 2)}%\n" \
                    f"闪避 (EVA): {self.convert(player_obj.eva * 100, 2)}%\n" \
                    f"=========="
        self.CQApi.send_group_message(from_group, from_qq, data_msg)
