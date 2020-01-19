#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.database.models.news

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import datetime

from django.db import models


class NewsManager(models.Manager):

    def get_news_by_url(self, url):
        return self.filter(url=url).first()

    def get_not_send_news(self):
        return self.filter(has_send=0).all()

    def get_today_news(self):
        today = datetime.datetime.today()
        return self.filter(
            created_time__day=today.day,
            created_time__year=today.year,
            created_time__month=today.month
        ).all()


class NewsModel(models.Model):
    class Meta:
        db_table = "baka_news"

    title = models.TextField(default="", null=False)
    url = models.TextField(default="", null=False)
    has_send = models.IntegerField(default=0, null=False)

    created_time = models.DateTimeField(auto_now=True)
    updated_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    instance = NewsManager()
