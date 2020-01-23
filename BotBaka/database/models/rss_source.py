#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.database.models.rss_source

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models


class RssSourceManager(models.Manager):

    def get_by_url(self, url):
        return self.filter(url=url).first()


class RssSourceModel(models.Model):
    class Meta:
        db_table = "baka_rss_source"

    name = models.TextField(default="", null=False)
    url = models.TextField(default="", null=False)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = RssSourceManager()
