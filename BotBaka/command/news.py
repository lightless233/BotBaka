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
from ..database.models import NewsModel
from ..utils.log import logger


class NewsCommand(BaseCommand):
    def __init__(self):
        super(NewsCommand, self).__init__()

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        # 从db中找到今天的新闻
        news = NewsModel.instance.get_today_news()
        logger.debug("news: {}".format(news))
        if not news:
            self.CQApi.send_group_message(from_group, from_qq, "今日暂无新闻！")
        else:
            msg = ["{}\n{}".format(n.title, n.url) for n in news]
            self.CQApi.send_group_message(from_group, from_qq, "\n\n".join(msg))
