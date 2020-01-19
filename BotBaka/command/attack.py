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
from typing import List

from .base import BaseCommand


class AttackCommand(BaseCommand):
    def __init__(self):
        super(AttackCommand, self).__init__()

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        pass
