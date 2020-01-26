#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.timer.regain
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import datetime
from typing import List

from django.db import transaction

from BotBaka.database.models import PlayerModel, PlayerRegainModel
from BotBaka.timer.engine.thread import SingleThreadEngine
from BotBaka.utils.log import logger


class GameRegainTimer(SingleThreadEngine):

    def __init__(self):
        super(GameRegainTimer, self).__init__()
        self.name = "game-regain-timer"

    def _worker(self):
        logger.info("{} start!".format(self.name))

        while self.is_running():

            self.ev.wait(30)

            # 1. 取出所有hp和sp不满的玩家
            players: List[PlayerModel] = PlayerModel.instance.get_no_full_hp_or_sp_player()

            logger.info("有{}个记录需要更新".format(len(players)))

            for _player in players:
                qq = _player.qq
                regain_obj = PlayerRegainModel.instance.filter(qq=qq).first()
                if regain_obj is None:
                    regain_obj = PlayerRegainModel.instance.create(qq=qq)

                current_time = datetime.datetime.now()

                logger.debug("next_hp_ts: {}, next_sp_ts: {}".format(regain_obj.next_hp_time, regain_obj.next_sp_time))

                max_hp = _player.max_hp
                current_hp = _player.current_hp
                if current_time > regain_obj.next_hp_time and current_hp < max_hp:
                    with transaction.atomic():
                        PlayerModel.instance.update_x("hp", qq)
                        PlayerRegainModel.instance.update_next_time("hp", qq)

                max_sp = _player.max_sp
                current_sp = _player.current_sp
                if current_time > regain_obj.next_sp_time and current_sp < max_sp:
                    with transaction.atomic():
                        PlayerModel.instance.update_x("sp", qq)
                        PlayerRegainModel.instance.update("sp", qq)
