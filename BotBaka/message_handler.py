#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.message_handler
    ~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import json
import re
import sys
import traceback
from typing import List, Optional, Dict

from BotBaka.api import CQApi
from BotBaka.command.admin_command import BanCommand, UnBanCommand, TitleCommand
from BotBaka.command.attack import AttackCommand
from BotBaka.command.base import BaseCommand
from BotBaka.command.misc_command import HelpCommand, ChangelogCommand
from BotBaka.command.news import NewsCommand
from BotBaka.command.invite import InviteAcceptCommand, InviteCommand, InviteGuCommand
from BotBaka.data.common_data import MessageMeta, PostType, SubType, MessageType
from BotBaka.pipeline.base import BasePipeline
from BotBaka.pipeline.repeat_checker import RepeatCheckerPipeline
from BotBaka.pipeline.ryuo import RyuoPipeline
from BotBaka.pipeline.thumb_checker import ThumbCheckerPipeline
from BotBaka.utils.log import logger


class MessageHandler:

    def __init__(self):
        super(MessageHandler, self).__init__()

        self.pipelines: List[BasePipeline] = [
            ThumbCheckerPipeline(),
            RepeatCheckerPipeline(),
            RyuoPipeline(),
        ]

        self.commands: Dict[str, BaseCommand] = {
            "%ban": BanCommand(),
            "%unban": UnBanCommand(),
            "%help": HelpCommand(),
            "%changelog": ChangelogCommand(),
            "%news": NewsCommand(),
            "%attack": AttackCommand(),
            "%title": TitleCommand(),
            "%invite": InviteCommand(),
            "%invite_accept": InviteAcceptCommand(),
            "%ia": InviteAcceptCommand(),
            "%invite_gu": InviteGuCommand(),
            "%ig": InviteGuCommand(),
        }

    def execute(self, message: str):
        obj: dict = json.loads(message)

        # 获取基础信息
        from_qq = obj.get(MessageMeta.USER_ID)
        from_group = obj.get(MessageMeta.GROUP_ID)

        if from_group not in [574255110, 672534169]:
            logger.error("No target group message: {}".format(from_group))
            return

        content = obj.get(MessageMeta.MESSAGE)
        # logger.debug("type of content: {}".format(type(content)))
        card = obj.get(MessageMeta.SENDER).get("card")
        nickname = obj.get(MessageMeta.SENDER).get("nickname")
        readable_name = card if card else nickname

        # 获取消息识别信息
        post_type = obj.get(MessageMeta.POST_TYPE)
        message_type = obj.get(MessageMeta.MESSAGE_TYPE)
        sub_type = obj.get(MessageMeta.SUB_TYPE)

        if post_type == PostType.MESSAGE:
            if message_type == MessageType.GROUP:
                if sub_type == SubType.NORMAL:
                    # 群聊消息
                    self.on_group_message(from_group, from_qq, readable_name, content, obj)
                    return
            elif message_type == MessageType.PRIVATE:
                # logger.warning("收到暂不支持的私聊消息，消息内容：{}，来源：{}".format(content, from_qq))
                return
            else:
                return
        else:
            return

    def on_group_message(self, from_group: int, from_qq: int, readable_name: str,
                         content: str, origin_msg: dict) -> None:
        logger.debug(
            "on_group_message, group: {}, qq: {}, name: {}, content: {}".format(
                from_group, from_qq, readable_name, content)
        )

        # start pipeline ＃
        should_continue = True
        for _pipeline in self.pipelines:
            result = _pipeline.process(from_group, from_qq, readable_name, content)
            should_continue = result
            if not should_continue:
                break
        # pipeline stop #

        if not should_continue:
            return

        if content.startswith("%"):
            command_list = re.split(r"\s+", content)
            input_command_name = command_list[0]
            command_instance: Optional[BaseCommand] = self.commands.get(input_command_name, None)
            if command_instance is None:
                # self.commands.get("%help").process(from_group, from_qq, readable_name, command_list)
                _api = CQApi()
                _api.send_group_message(from_group, from_qq, "Unknown Command!")
            else:
                try:
                    command_instance.process(from_group, from_qq, readable_name, command_list)
                except Exception as e:
                    tbe = traceback.TracebackException(*sys.exc_info())
                    full_err = ''.join(tbe.format())
                    CQApi().send_group_message(from_group, from_qq, "Unknown Error! e: {}\n{}".format(e, full_err))
