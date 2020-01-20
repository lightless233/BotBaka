#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.database.models.last_ryuo

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
from django.db import models


class LastRyuoManager(models.Manager):

    def get_latest_ryuo(self):
        return self.filter().order_by('-created_time').first()


class LastRyuoModel(models.Model):
    """
    记录每一天的龙王信息
    """

    class Meta:
        db_table = "baka_last_ryuo"

    qq = models.BigIntegerField(default=0, null=False)
    cnt = models.IntegerField(default=0, null=False)
    nickname = models.TextField(default="", null=False)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = LastRyuoManager()
