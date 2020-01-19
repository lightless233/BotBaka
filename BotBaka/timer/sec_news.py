#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.pipeline.thumb_checker
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from typing import List

import requests
from bs4 import BeautifulSoup

from .engine.thread import SingleThreadEngine
from ..database.models.news import NewsModel
from ..utils.log import logger


class SecNewsTimer(SingleThreadEngine):

    def __init__(self):
        super(SecNewsTimer, self).__init__()

        self.target_url = "https://sec.today/pulses/"
        self.target_group = 672534169

        self.name = "secnews-timer"

    def _worker(self):

        logger.debug("SecNewsTimer start!")

        while self.is_running():

            response = requests.get(self.target_url, timeout=12)
            page_content = response.text

            # 筛选数据
            soup = BeautifulSoup(page_content)
            articles = soup.find_all("div", "my-2")

            for x in articles:
                tag_a = x.find_all("a")[0]
                href = tag_a["href"]
                full_url = "https://sec.today/" + href[1:]
                title = tag_a.text

                logger.info("href: {}, title: {}".format(full_url, title))

                # 检查这个新闻有没有入过库了
                # 如果没有，就入库
                # 如果已经入库了，那么看看有没有发送过了，如果没发过就发出去，并更新状态
                self.save(title, full_url)

            self.send_and_update()

            self.ev.wait(300)

    def save(self, title: str, full_url: str):
        # todo：多个SQL改成原子操作
        news = NewsModel.instance.get_news_by_url(url=full_url)
        if news is None:
            # 新的数据，存起来
            NewsModel.instance.create(url=full_url, title=title, has_send=0)

    def send_and_update(self):
        # todo：多个SQL改成原子操作
        all_news: List[NewsModel] = NewsModel.instance.get_not_send_news()
        for news in all_news:
            msg = news.title + "\n" + news.url
            self.CQApi.send_group_message(self.target_group, None, msg)

            # 更新状态
            news.has_send = 1
            news.save()
