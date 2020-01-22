#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.database.models.ryuo

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import datetime

from django.db import models

from BotBaka.utils.log import logger


class RyuoManager(models.Manager):
    def get_today_user_by_qq(self, qq):
        today = datetime.datetime.today()

        return self.filter(
            qq=qq,
            created_time__year=today.year,
            created_time__month=today.month,
            created_time__day=today.day
        ).first()

    def get_today_cnt(self):
        now = datetime.datetime.now()
        start = now - datetime.timedelta(hours=24)

        ret_value = {}

        results = self.filter(updated_time__gte=start, updated_time__lte=now).all()
        for res in results:
            nickname = res.nickname
            qq = res.qq
            cnt = res.cnt

            if qq not in ret_value:
                ret_value[qq] = {"nickname": nickname, "cnt": cnt}
            else:
                ret_value[qq] = {"nickname": nickname, "cnt": ret_value.get(qq).get("cnt") + cnt}

        # 排序
        sorted_res = sorted(ret_value.items(), key=lambda d: d[1]["cnt"])
        sorted_res.reverse()

        return sorted_res


class RyuoModel(models.Model):
    class Meta:
        db_table = "baka_ryuo"

    qq = models.BigIntegerField(default=0, null=False)
    cnt = models.IntegerField(default=0, null=False)
    nickname = models.TextField(default="", null=False)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = RyuoManager()
