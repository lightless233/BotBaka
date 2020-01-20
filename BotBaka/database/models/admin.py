#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.database.models.admin

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models


class AdminUserManager(models.Manager):

    def add_admin(self, qq):
        return self.create(qq=qq)

    def remove_admin(self, qq):
        return self.filter(qq=qq).delete()


class AdminUserModel(models.Model):
    """
    记录所有的 管理员
    """

    class Meta:
        db_table = "baka_admin"

    qq = models.BigIntegerField(default=0, null=False)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = AdminUserManager()
