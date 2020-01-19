#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.data.CommonData
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""


class PostType:
    MESSAGE = "message"
    NOTICE = "notice"
    REQUEST = "request"
    META_EVENT = "meta_event"


class MessageType:
    GROUP = "group"
    PRIVATE = "private"


class SubType:
    NORMAL = "normal"
    ANONYMOUS = "anonymous"
    NOTICE = "notice"


class MessageMeta:
    POST_TYPE = "post_type"
    MESSAGE_TYPE = "message_type"
    SUB_TYPE = "sub_type"
    MESSAGE_ID = "message_id"
    GROUP_ID = "group_id"
    USER_ID = "user_id"
    ANONYMOUS = "anonymous"
    MESSAGE = "message"
    RAW_MESSAGE = "raw_message"
    FONT = "font"
    SENDER = "sender"
