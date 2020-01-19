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

from .base import BaseCommand
from ..utils.quick_at import QuickAt


class BanCommand(BaseCommand):

    def __init__(self):
        super(BanCommand, self).__init__()
        self.command_name = "%ban"

        self.err_msg = "Error arguments.\n%ban qq duration(min.)"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        if not self._check_admin(from_group, from_qq):
            return

        try:
            target_qq = command_list[1]
            duration = int(command_list[2])
        except (IndexError, ValueError):
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        qq = QuickAt.get_qq_from_at_msg(target_qq)
        if qq is None:
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        self.CQApi.set_group_ban(from_group, qq, duration)
        self.CQApi.send_group_message(from_group, from_qq, "%ban success.")


class UnBanCommand(BaseCommand):

    def __init__(self):
        super(UnBanCommand, self).__init__()
        self.command_name = "%unban"
        self.err_msg = "Error arguments.\n%unban qq"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        if not self._check_admin(from_group, from_qq):
            return

        try:
            target_qq = command_list[1]
        except (IndexError, ValueError):
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        qq = QuickAt.get_qq_from_at_msg(target_qq)
        if qq is None:
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        self.CQApi.set_group_ban(from_group, qq, 0)
        self.CQApi.send_group_message(from_group, from_qq, "%unban success.")
