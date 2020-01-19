#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.admin_command
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from typing import List

from BotBaka.command.base import BaseCommand

help_msg = """BotBaka version 1.0.2

--- 普通命令 ---
%help - 显示这个页面
%attack - 攻击某个玩家，格式：%attack @目标 时长(分钟)
%game - 游戏命令
%news - 每日新闻 (Author: WinFog)
---------------

--- Admin命令 ---
%ban - 干掉指定人，格式：%ban @目标 时长(分钟)
%unban - 解封指定人，格式：%unban @目标
---------------

--- 其他信息 ---
项目地址：https://github.com/lightless233/BotXYZ
Bug、Request报告地址：https://github.com/lightless233/BotXYZ/issues
---------------
"""

changelog = """v1.0.2
- 增加 %news 功能 (Author: WinFog)
- 增加 %game 功能 (under developing)

v1.0.1
- 削弱%attack时的见切机制
- 削弱%attack时的debuff效果
- 程序框架重构，方便多人开发

v1.0.0
- 基本框架完成
- 新增%ban、%unban、%attack命令
"""


class HelpCommand(BaseCommand):

    def __init__(self):
        super(HelpCommand, self).__init__()

        self.command_name = "%help"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        self.CQApi.send_group_message(from_group, from_qq, help_msg)


class ChangelogCommand(BaseCommand):

    def __init__(self):
        super(ChangelogCommand, self).__init__()

        self.command_name = "%changelog"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        self.CQApi.send_group_message(from_group, from_qq, changelog)
