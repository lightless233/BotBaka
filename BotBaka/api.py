#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.api
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import requests

from BotBaka.utils.log import logger
from BotBaka.utils.quick_at import QuickAt


class CQApi:

    def __init__(self):
        super(CQApi, self).__init__()

        self.base_url = "http://localhost:5700"

        self.api_list = {
            "set_group_ban": self.base_url + "/set_group_ban",
            "set_group_ban_async": self.base_url + "/set_group_ban_async",
            "send_group_message": self.base_url + "/send_group_msg",
            "send_group_message_async": self.base_url + "/send_group_msg_async",
        }

        self.token = "GKMFZWDQ2011"

    def _call(self, method: str, params: dict):
        url = self.api_list.get(method)
        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }
        response = requests.post(url, json=params, headers=headers)
        logger.debug("call response: {}".format(response.content))

    def set_group_ban(self, group: int, qq: int, duration: int, use_async=True):
        if use_async:
            method_name = "set_group_ban_async"
        else:
            method_name = "set_group_ban"

        params = {
            "group_id": group,
            "user_id": qq,
            "duration": int(duration * 60)
        }

        logger.debug("set_group_ban params: {}".format(params))

        self._call(method_name, params)

    def send_group_message(self, group: int, qq: int, message: str, auto_at=True, use_async=True):
        if use_async:
            method_name = "send_group_message_async"
        else:
            method_name = "send_group_message"

        if auto_at and qq is not None:
            at_message = QuickAt.build_at_msg(qq)
        else:
            at_message = ""

        params = {
            "group_id": group,
            "message": message if at_message == "" else at_message + "\n" + message
        }

        self._call(method_name, params)
