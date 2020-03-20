#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.utils.notification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    通知类工具，当bot出现错误时，可以通过此工具类发送错误通知

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from traceback import TracebackException

from BotBaka.api import CQApi


class ErrorNotification:

    @staticmethod
    def send(receiver: int, tbe: TracebackException, e: Exception, api_instance: CQApi = None):
        """
        给指定人发送异常日志消息

        @param receiver: 消息接收人
        @param tbe: 带tb的异常
        @param e: 异常
        @param api_instance:

        @rtype: bool
        """

        api = api_instance if api_instance is not None else CQApi()

        full_error = "Exception: {}\n\nFull traceback:\n{}".format(
            e, "".join(tbe.format())
        )

        api.send_private_message(receiver, full_error)
