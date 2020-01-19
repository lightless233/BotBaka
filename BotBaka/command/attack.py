#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.attack
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import math
import random
import time
from typing import List

from .base import BaseCommand
from ..utils.log import logger
from ..utils.quick_at import QuickAt

shield_time = {}
code_time = {}


class AttackCommand(BaseCommand):
    def __init__(self):
        super(AttackCommand, self).__init__()

        self.command_name = "%attack"

        self.err_msg = "Error arguments.\n%attack qq duration(min.)"

    def ban(self, is_stake, from_group, from_qq, duration):
        if is_stake:
            return

        self.CQApi.set_group_ban(from_group, from_qq, duration)

    def update_shield(self, qq, duration, attacker):
        global shield_time
        if attacker:
            shield_time[qq] = int(time.time()) + (1.5 * (duration / 2) * 60)
        else:
            shield_time[qq] = int(time.time()) + (2 * (duration / 2) * 60)

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        global shield_time, code_time

        try:
            target_qq = command_list[1]
            duration = command_list[2]
        except IndexError:
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        target_qq = QuickAt.get_qq_from_at_msg(target_qq)
        if target_qq is None:
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        try:
            real_target = int(target_qq)
            duration = int(duration)
        except Exception:
            logger.error("Error argument.")
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        at_attacker_qq_msg = QuickAt.build_at_msg(from_qq)
        at_target_qq_msg = QuickAt.build_at_msg(real_target)
        is_stake = False

        # 校验参数
        if duration < 0:
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        if duration == 0:
            self.CQApi.send_group_message(from_group, from_qq, "彩蛋已经修复咯！")
            self.CQApi.set_group_ban(from_group, from_qq, 60 * 60)
            return

        # 如果这个傻子要打自己
        if int(real_target) == from_qq:
            # self.CQApi.set_group_ban(from_group, from_qq, duration * 60)
            self.CQApi.send_group_message(from_group, from_qq, "不可以打自己哦！")
            return

        # 如果打群主
        # 群主作为木桩人使用
        if int(real_target) == 2522031536:
            # self.api.set_group_ban(from_group, from_qq, duration * 60 * 2)
            # self.api.send_group_msg(from_group, at_attacker_qq_msg + "\n二营长，你他娘的意大利炮呢？给老子拉上来！开炮！开炮！开炮！")
            is_stake = True

        # 检查CD有没有转好
        t = code_time.get(from_qq)
        if t is not None:
            if t > int(time.time()):
                self.CQApi.send_group_message(from_group, from_qq, "CD还没转好哦，不能搞这么快哦！")
                return
            else:
                code_time[from_qq] = time.time() + 60 * 1
        else:
            code_time[from_qq] = time.time() + 60 * 1
            pass

        # 检查被害人是否有护盾时间
        t = shield_time.get(real_target)
        if t is not None and t > int(time.time()):
            self.CQApi.send_group_message(from_group, from_qq, "目标玩家有护盾呢！")
            return

        # 检查攻击方是否有有效盾，如果有盾就破盾
        t = shield_time.get(from_qq)
        if t is not None and t > int(time.time()):
            self.CQApi.send_group_message(from_group, from_qq, "主动攻击，己方护盾失效！")
            shield_time[from_qq] = -1

        # 正常攻击，先开始roll点
        attacker_pt = random.randint(0, 100)
        target_pt = random.randint(0, 100)

        base_msg = at_attacker_qq_msg + f"的点数：{attacker_pt}\n"
        base_msg += at_target_qq_msg + f"的点数：{target_pt}\n"

        # 如果俩人点数相等，统统干掉，但是时间减半
        # 如果攻击者和目标都是100点，统统禁言，并且翻倍时间
        if attacker_pt == target_pt and attacker_pt != 100:
            base_msg += "旗鼓相当的对手，两败俱伤！"
            self.CQApi.send_group_message(from_group, from_qq, base_msg)

            self.ban(is_stake, from_group, from_qq, duration / 2)
            self.ban(is_stake, from_group, real_target, duration / 2)

            # 获得护盾
            # shield_time[from_qq] = int(time.time()) + (1.5 * (duration / 2) * 60)
            # shield_time[real_target] = int(time.time()) + (2 * (duration / 2) * 60)
            self.update_shield(from_qq, duration / 2, True)
            self.update_shield(real_target, duration / 2, False)

            return

        if attacker_pt == target_pt and attacker_pt == 100:
            base_msg += "你俩怎么一起开大招？"
            self.CQApi.send_group_message(from_group, from_qq, base_msg)
            self.ban(is_stake, from_group, from_qq, duration * 2)
            self.ban(is_stake, from_group, real_target, duration * 2)

            # 获得护盾
            self.update_shield(from_qq, duration * 2, True)
            self.update_shield(real_target, duration * 2, False)

            return

        # 如果攻击者roll到100点，无视防御
        if attacker_pt == 100 and target_pt != 100:
            base_msg += at_attacker_qq_msg + "居然开大了！无视防御！双倍伤害！"
            self.CQApi.send_group_message(from_group, from_qq, base_msg)
            self.ban(is_stake, from_group, real_target, duration * 2)

            # 受害者获得护盾
            self.update_shield(real_target, duration * 2, False)

            return

        # 如果目标roll到了100点，无视攻击
        if target_pt == 100 and attacker_pt != 100:
            base_msg += at_attacker_qq_msg + "发动了：绝 对 防 御，并且反击成功！"
            self.CQApi.send_group_message(from_group, from_qq, base_msg)
            self.ban(is_stake, from_group, from_qq, duration)

            # 攻击者获得一半护盾
            self.update_shield(from_qq, duration, True)

            return

        # todo: 处理一下roll到0点的情况
        final_attacker_pt = math.floor(attacker_pt - (duration / 60) * 50 * ((random.randint(0, 10) + 5) / 20))

        base_msg = at_attacker_qq_msg + f"的点数：{attacker_pt}，叠加 debuff 后的点数：{final_attacker_pt}\n"
        base_msg += at_target_qq_msg + f"的点数：{target_pt}\n"
        can_counter = False
        if final_attacker_pt > target_pt:
            # 攻击成功
            base_msg += at_attacker_qq_msg + "的攻击得手了！"
            self.ban(is_stake, from_group, real_target, duration)
            self.CQApi.send_group_message(from_group, from_qq, base_msg)

            self.update_shield(real_target, duration, False)

        elif final_attacker_pt < target_pt:
            # 攻击失败
            base_msg += at_attacker_qq_msg + "手滑了，啥也没打到。"
            self.CQApi.send_group_message(from_group, from_qq, base_msg)
            can_counter = True
        else:
            # 相等了
            base_msg += "旗鼓相当的对手，两败俱伤，伤害均摊。"
            self.CQApi.send_group_message(from_group, from_qq, base_msg)
            self.ban(is_stake, from_group, real_target, duration / 2)
            self.ban(is_stake, from_group, from_qq, duration / 2)

            self.update_shield(real_target, duration / 2, False)
            self.update_shield(from_qq, duration / 2, True)

        # 开始反击判定
        if not can_counter:
            return
        # 临时patch，在大时长下增强见切概率
        if 10 <= duration <= 20:
            counter_attack_pt = math.floor(random.randint(0, 100) * 1.0)
        elif duration >= 20:
            counter_attack_pt = math.floor(random.randint(0, 100) * 1.2)
        else:
            counter_attack_pt = math.floor(random.randint(0, 100) * 1.0)
        logger.info(f"counter_attack_pt: {counter_attack_pt}")
        if counter_attack_pt > final_attacker_pt:
            # 反击成功
            self.CQApi.send_group_message(from_group, from_qq, f"见切成功！斩于马下！反击值：{counter_attack_pt}")
            self.ban(is_stake, from_group, from_qq, duration * 0.6)
            self.update_shield(from_qq, duration * 0.6, True)
        else:
            # 反击失败
            self.CQApi.send_group_message(from_group, from_qq, f"反击失败了，真可惜。反击值：{counter_attack_pt}")
