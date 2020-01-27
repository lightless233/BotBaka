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
    every_hp_value = 10
    every_sp_value = 1

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
            new_properties = GameTools.calc_properties(_player.level, _player.base_str, _player.base_vit,
                                                       _player.base_agi)
            return PlayerModel.instance.filter(qq=qq).update(
                max_hp=new_properties.get("hp"),
                max_sp=new_properties.get("sp"),
                atk=new_properties.get("atk"),
                defend=new_properties.get("def"),
                cri=new_properties.get("cri"),
                hit=new_properties.get("hit"),
                eva=new_properties.get("eva"),
            )

    def get_no_full_hp_or_sp_player(self):
        return self.exclude(max_hp=F("current_hp"), max_sp=F("current_sp")).all()

    def update_x(self, x, qq):
        with transaction.atomic():
            _player: PlayerModel = self.filter(qq=qq).first()
            if _player is None:
                return

            if x == "hp":
                v = PlayerManager.every_hp_value if \
                    _player.max_hp - _player.current_hp > PlayerManager.every_hp_value else \
                    _player.max_hp - _player.current_hp
                _player.current_hp += v
            elif x == "sp":
                v = PlayerManager.every_sp_value if \
                    _player.max_sp - _player.current_sp > PlayerManager.every_sp_value else \
                    _player.max_sp - _player.current_sp
                _player.current_sp += v
            else:
                return
            _player.save()

    def update_sp_by_skill(self, attacker, skill_name):
        _obj: PlayerModel = self.filter(qq=attacker).first()
        if _obj is None:
            return

        if skill_name is None:
            _obj.current_sp -= 1
            _obj.save()
        else:
            # todo skill 实装的时候需要修改
            return

    def is_player_alive(self, qq):
        _obj: PlayerModel = self.filter(qq=qq).first()
        if _obj is None:
            return

        return _obj.current_hp != 0


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
    cri = models.FloatField(default=GameBaseInitData.BASE_CRI)
    hit = models.FloatField(default=GameBaseInitData.BASE_HIT)
    eva = models.FloatField(default=GameBaseInitData.BASE_EVA)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = PlayerManager()


# ====================

class PlayerRegainManager(models.Manager):
    hp_timedelta = 10
    sp_timedelta = 5
    resurrect_timedelta = 60 * 6

    def update_next_time(self, target, qq):

        with transaction.atomic():

            _obj: PlayerRegainModel = self.filter(qq=qq).first()
            if _obj is None:
                return

            if target == "hp":
                _obj.next_hp_time = datetime.datetime.now() + datetime.timedelta(
                    minutes=PlayerRegainManager.hp_timedelta)

            elif target == "sp":
                _obj.next_sp_time = datetime.datetime.now() + datetime.timedelta(
                    minutes=PlayerRegainManager.sp_timedelta)
            else:
                return

            _obj.save()


class PlayerRegainModel(models.Model):
    class Meta:
        db_table = "baka_player_regain"

    qq = models.PositiveIntegerField(default=0, null=False)
    next_hp_time = models.DateTimeField(default=datetime.datetime.now)
    next_sp_time = models.DateTimeField(default=datetime.datetime.now)
    next_resurrect_time = models.DateTimeField(default=datetime.datetime.now)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    instance = PlayerRegainManager()
