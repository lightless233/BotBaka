#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.web.controller.event
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""

from django.http import HttpResponse
from django.views import View

from BotBaka.message_handler import MessageHandler
from BotBaka.utils.log import logger

"""
    接受bot返回的事件，消息样例
    消息格式可以参考：https://cqhttp.cc/docs/4.13/#/Post
    {
    "anonymous": null,
    "font": 9307096,
    "group_id": 672534169,
    "message":"\xe4\xbd\xa0\xe4\xb8\x8d\xe6\x98\xaf\xef\xbc\x8c\xe7\xbb\x93\xe5\xa9\x9a\xe4\xb8\x8b\xe8\xbe\x88\xe5\xad\x90\xef\xbc\x8c\xe5\xa5\xb3\xe6\x9c\x8b\xe5\x8f\x8b\xe8\xbf\x99\xe8\xbe\x88\xe5\xad\x90\xe5\x90\x97",
    "message_id": 12286,
    "message_type": "group",
    "post_type": "message",     // 指示此次上报的类型，message - 消息、notice - 群、讨论组变动通知、request - 好友、加群请求
    "raw_message":"\xe4\xbd\xa0\xe4\xb8\x8d\xe6\x98\xaf\xef\xbc\x8c\xe7\xbb\x93\xe5\xa9\x9a\xe4\xb8\x8b\xe8\xbe\x88\xe5\xad\x90\xef\xbc\x8c\xe5\xa5\xb3\xe6\x9c\x8b\xe5\x8f\x8b\xe8\xbf\x99\xe8\xbe\x88\xe5\xad\x90\xe5\x90\x97",
    "self_id": 2522031536,
    "sender": {
        "age": 7,
        "area":"\xe9\x98\xbf\xe5\xaf\x8c\xe6\xb1\x97",
        "card":"\xe7\xbe\xa4\xe5\x80\x92\xe6\x95\xb0\xe7\xac\xac\xe4\xb8\x80",
        "level":"\xe8\xaf\x9d\xe5\x94\xa0",
        "nickname": "lightless",
        "role": "member",
        "sex": "male",
        "title": "",
        "user_id": 387210935
    },
    "sub_type": "normal",
    "time": 1579422412,
    "user_id": 387210935
}
"""


class EventView(View):

    def __init__(self):
        super(EventView, self).__init__()
        self.__message_handler = MessageHandler()

    def post(self, request):
        logger.debug("Receive post data: {}".format(request.body))
        self.__message_handler.execute(request.body)
        return HttpResponse("")
