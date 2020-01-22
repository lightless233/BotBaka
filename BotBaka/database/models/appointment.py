#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.database.models.appointment

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""
import datetime

from django.db import models
from django.db.models import Q


class AppointmentManager(models.Manager):

    def get_event_by_id(self, event_id):
        return self.get(id=event_id)

    def get_all_active_event(self):
        return self.filter(~Q(has_end=1)).all()


class AppointmentUserManager(models.Manager):

    def get_invited_user_by_id(self, event_id):
        return self.filter(event_id=event_id).all()

    def get_user(self, event_id, user_id):
        return self.filter(event_id=event_id, user_id=user_id).first()

    def get_gu_user(self):
        return self.filter(gu=1, has_title=0).all()


class AppointmentModel(models.Model):
    class Meta:
        db_table = "baka_appointment"

    event_name = models.TextField(default="", null=False)
    event_time = models.DateTimeField(default=datetime.datetime.now, null=False)
    has_end = models.SmallIntegerField(default=0, null=False)
    organizer = models.BigIntegerField(default=0, null=False)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = AppointmentManager()


class AppointmentUserModel(models.Model):
    class Meta:
        db_table = "baka_appointment_user"

    event_id = models.BigIntegerField(default=0, null=False)
    user_id = models.BigIntegerField(default=0, null=False)
    accepted = models.SmallIntegerField(default=-1, null=False)
    gu = models.SmallIntegerField(default=-1, null=False)
    title_end_time = models.DateTimeField(default=datetime.datetime.now, null=False)
    has_title = models.SmallIntegerField(default=0, null=False)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = AppointmentUserManager()
