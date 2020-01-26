#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.database.models.player
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import datetime

from django.db import models, transaction
from django.db.models import F

from BotBaka.data import GameBaseInitData
from BotBaka.utils.game_tools import GameTools


class PlayerManager(models.Manager):
    def get_player_by_qq(self, qq: int):
        return self.filter(qq=qq).first()

    def update_player_prop(self, qq, prop, pt):
        with transaction.atomic():
            query = self.filter(qq=qq)
            if prop == "STR":
                query = query.update(base_str=F("base_str") + pt, rest_pt=F("rest_pt") - pt)
            elif prop == "AGI":
                query = query.update(base_agi=F("base_agi") + pt, rest_pt=F("rest_pt") - pt)
            elif prop == "VIT":
                query = query.update(base_vit=F("base_vit") + pt, rest_pt=F("rest_pt") - pt)

            # 根据一级属性，重新计算二级属性，并且更新到记录中
            _player: PlayerModel = self.filter(qq=qq).first()
            new_properties = GameTools.calc_properties(_player.level, _player.base_str, _player.base_vit, _player.base_agi)
            return PlayerModel.instance.filter(qq=qq).update(
                max_hp=new_properties.get("hp"),
                max_sp=new_properties.get("sp"),
                atk=new_properties.get("atk"),
                defend=new_properties.get("def"),
                cri=new_properties.get("cri"),
                hit=new_properties.get("hit"),
                eva=new_properties.get("eva"),
            )


class PlayerModel(models.Model):
    class Meta:
        db_table = "baka_player"

    # 基本信息
    qq = models.BigIntegerField(default=0, null=False)
    level = models.PositiveSmallIntegerField(default=1, null=False)
    rest_pt = models.PositiveIntegerField(default=3, null=False)

    # 当前的经验值，每升一级就清零一次
    exp = models.PositiveIntegerField(default=0, null=False)

    # 一级属性
    base_str = models.PositiveIntegerField(default=0, null=False)
    base_vit = models.PositiveIntegerField(default=0, null=False)
    base_agi = models.PositiveIntegerField(default=0, null=False)
    base_luk = models.PositiveIntegerField(default=0, null=False)

    # 二级属性
    max_hp = models.PositiveIntegerField(default=GameBaseInitData.BASE_HP)
    current_hp = models.PositiveIntegerField(default=GameBaseInitData.BASE_HP)

    max_sp = models.PositiveIntegerField(default=GameBaseInitData.BASE_SP)
    current_sp = models.PositiveIntegerField(default=GameBaseInitData.BASE_SP)

    atk = models.PositiveIntegerField(default=GameBaseInitData.BASE_ATK)
    defend = models.PositiveIntegerField(default=GameBaseInitData.BASE_DEF)
    cri = models.PositiveIntegerField(default=GameBaseInitData.BASE_CRI)
    hit = models.PositiveIntegerField(default=GameBaseInitData.BASE_HIT)
    eva = models.PositiveIntegerField(default=GameBaseInitData.BASE_EVA)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = PlayerManager()


# ====================

class PlayerRegainManager(models.Manager):
    pass


class PlayerRegainModel(models.Model):
    class Meta:
        table_name = "baka_player_regain"

    qq = models.PositiveIntegerField(default=0, null=False)
    next_hp_time = models.DateTimeField(default=datetime.datetime.now)
    next_sp_time = models.DateTimeField(default=datetime.datetime.now)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = PlayerRegainManager()
