#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.timer.attack
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import random
from typing import List

from ..base import BaseCommand
from ...data.game_data import AttackParams
from ...database.models import PlayerModel
from ...utils import GameTools
from ...utils.log import logger
from ...utils.quick_at import QuickAt


class AttackSubCommand(BaseCommand):
    """
    %game attack @target [skill_name] 如果skill_name不指定，则为普通攻击

    > 相关数据操作需要在一个事务中完成 ！！！

    结算步骤
        1. 检查目标是否存活 (HP为0的玩家是死亡状态，可以被奶起来或者特定道具救活，否则需要6小时自然恢复)
        2. 检查攻击方的SP点数
        3. 伤害结算
            3.0 SP结算
            3.1 命中计算
            3.2 暴击结算
            3.3 伤害结算
        4. 经验结算
            4.1 升级结算
            每一级的升级所需要经验：exp = (level - 1) * 20 + 100
            例如，从1级升级到2级，需要exp = (1-1) * 20 + 100
        5. 死亡结算
        6. 道具掉落结算
    """

    def __init__(self):
        super(AttackSubCommand, self).__init__()

        self.command_name = "%game attack"
        self._err_tips = "%game attack @target [skill_name] 如果skill_name不指定，则为普通攻击"

        self.message_no_hit = """【战斗结算】
{attacker} 对 {target} 发动了 [{skill_name}]
{target} 成功闪避，未击中。
"""
        self.message = """【战斗结算】
{attacker} 对 {target} 发动了 [{skill_name}]
造成了 {dmg} 点{cri}伤害。{dead}
"""

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        # 0. 获取参数
        try:
            target_qq = command_list[2]
            target_qq = QuickAt.get_qq_from_at_msg(target_qq)
            if target_qq is None:
                self.CQApi.send_group_message(from_group, from_qq, "格式错误：{}".format(self._err_tips))
                return
        except IndexError:
            self.CQApi.send_group_message(from_group, from_qq, "格式错误：{}".format(self._err_tips))
            return

        try:
            skill_name = command_list[3]
        except IndexError:
            # 没有指定技能名称，普通攻击
            skill_name = None

        # 获取双方的实例
        attacker_obj: PlayerModel = PlayerModel.instance.get_player_by_qq(from_qq)
        target_obj: PlayerModel = PlayerModel.instance.get_player_by_qq(target_qq)
        if attacker_obj is None or target_obj is None:
            self.CQApi.send_group_message(from_group, from_qq, "格式错误：{}".format(self._err_tips))
            return

        # 1. 检查目标是否存活
        if not PlayerModel.instance.is_player_alive(target_qq):
            self.CQApi.send_group_message(from_group, from_qq, "目标玩家已经死亡！")
            return

        # 2. 检查攻击方的 SP 点数
        attacker = from_qq
        has_enough_sp = PlayerModel.instance.is_player_has_enough_sp(attacker, skill_name)
        if not has_enough_sp:
            self.CQApi.send_group_message(
                from_group, from_qq,
                "SP不足，无法发动 [{}]".format(skill_name if skill_name is not None else "普通攻击")
            )
            return

        # 3. 伤害结算
        # 3.0 SP结算
        PlayerModel.instance.update_sp_by_skill(attacker, skill_name)

        # 3.1 命中计算
        # 公式：攻击者命中 / (攻击者命中 + 敌方闪避) + D20随机值
        d20 = GameTools.d20() / 100
        final_hit = attacker_obj.hit / (attacker_obj.hit + target_obj.eva) + d20
        judge = random.random()
        logger.debug("命中计算：judge: {}, d20: {}, final_hit: {}".format(judge, d20, final_hit))
        if judge > final_hit:
            # 未命中，立即结算战斗
            self.CQApi.send_group_message(
                from_group, from_qq,
                self.message_no_hit.format(
                    attacker=QuickAt.build_at_msg(from_qq),
                    target=QuickAt.build_at_msg(target_qq),
                    skill_name=skill_name if skill_name is not None else "普通攻击"
                )
            )
            return

        # 3.2 暴击结算
        # 公式：攻击者暴击 / (攻击者暴击 + 敌方闪避修正值) + D4
        # 敌方闪避修正 = 敌方闪避 IF 敌方闪避 >= 0.1 ELSE 敌方闪避*2
        d4 = GameTools.d4() / 100
        target_eva_fix = target_obj.eva if target_obj.eva >= 0.1 else target_obj.eva * 2
        final_cri = attacker_obj.cri / (attacker_obj.cri + target_eva_fix) + d4
        judge = random.random()
        logger.debug("暴击结算：judge: {}, d4: {}, final_cri: {}".format(judge, d4, final_cri))
        if judge > final_cri:
            # 未暴击，正常伤害
            has_cri = False
        else:
            has_cri = True
        logger.debug("暴击结算: has_cri: {}".format(has_cri))

        # 3.3 伤害结算
        # 先计算基础伤害，如果有暴击，那么在基础伤害上计算暴击伤害
        # 基础伤害公式：(攻击力 * 攻击力 * k1 + k2) / (攻击力 + 目标防御力*k3 + k4) + D20
        # 暴击伤害公式：基础伤害 * (1+暴击系数) + D20
        d20 = GameTools.d20()
        final_base_dmg = (attacker_obj.atk * attacker_obj.atk * AttackParams.K1 + AttackParams.K2) / \
                         (attacker_obj.atk + target_obj.defend * AttackParams.K3 + AttackParams.K4) + d20
        logger.debug("伤害结算（基础）: d20: {}, final_base_dmg: {}".format(d20, final_base_dmg))
        if has_cri:
            # 暴击伤害结算
            d20 = GameTools.d20()
            final_dmg = final_base_dmg * (1 + AttackParams.CRI_PARAM) + d20
        else:
            final_dmg = final_base_dmg
        logger.debug("final_dmg: {}".format(final_dmg))

        # 3.4 最终伤害以及死亡结算
        rest_hp = target_obj.current_hp - final_dmg
        if rest_hp <= 0:
            # 嗝屁了
            has_dead = True
            target_obj.current_hp = 0
        else:
            # 还活着
            has_dead = False
            target_obj.current_hp = rest_hp
        target_obj.save()

        # 4. 经验结算
        # 攻击成功，获得16点经验，成功击杀，获得32点经验
        level_up = False
        if has_dead:
            attacker_obj.exp += 32
        else:
            attacker_obj.exp += 16
        # 4.1 升级结算
        if attacker_obj.exp >= (attacker_obj.level - 1) * 20 + 100:
            # 升级了
            attacker_obj.exp = attacker_obj.exp - (attacker_obj.level - 1) * 20 + 100
            attacker_obj.level += 1
            attacker_obj.rest_pt += 3
            level_up = True

        attacker_obj.save()

        # 5. TODO 奖励结算

        # 6. 发送战况
        self.CQApi.send_group_message(
            from_group, from_qq,
            self.message.format(
                attacker=QuickAt.build_at_msg(from_qq),
                target=QuickAt.build_at_msg(target_qq),
                skill_name=skill_name if skill_name is not None else "普通攻击",
                dmg=final_dmg,
                cri="暴击" if has_cri else "",
                dead="目标已被击杀。" if has_dead else "",
            )
        )
        if level_up:
            self.CQApi.send_group_message(
                from_group, from_qq,
                "Level Up！请记得分配属性点。"
            )
