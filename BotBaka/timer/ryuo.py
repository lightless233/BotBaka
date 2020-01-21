#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.timer.ryuo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import datetime

from BotBaka.database.models import RyuoModel, AdminUserModel
from BotBaka.database.models.last_ryuo import LastRyuoModel
from BotBaka.timer.engine.thread import SingleThreadEngine
from BotBaka.utils.log import logger
from BotBaka.utils.quick_at import QuickAt


class RyuoTimer(SingleThreadEngine):

    def __init__(self):
        super(RyuoTimer, self).__init__()

        self.name = "ryuo-timer"

        self.target_group = 672534169

    def _worker(self):

        logger.debug("{} start.".format(self.name))

        while self.is_running():

            # 判断当前时间是否为凌晨7点
            # windows上没有好用的crontab，所以只能每隔1分钟进行一次判断
            now = datetime.datetime.now()
            if now.hour == 7 and now.minute == 5:

                logger.info("Ryuo timer work!")

                # 从db中获取前24个小时的发言内容
                results: list = RyuoModel.instance.get_today_cnt()
                ryuo = results[0]
                ryuo_qq = ryuo[0]
                ryuo_nickname = ryuo[1].get("nickname")
                ryuo_cnt = ryuo[1].get("cnt")

                logger.debug("ryuo: {}".format(ryuo))

                message = "昨日群内发言统计：\n"
                for qq, data in results:
                    message += "{}({}) -> {}\n".format(data["nickname"], qq, data["cnt"])
                message += "\n恭喜{}获得喷水龙的称号，获取管理员权限一天！\n来喷个水给大家康康。".format(QuickAt.build_at_msg(ryuo[0]))

                # 获取前一天的龙王
                last_ryuo = LastRyuoModel.instance.get_latest_ryuo()

                # 把龙王信息存起来
                LastRyuoModel.instance.create(qq=ryuo_qq, cnt=ryuo_cnt, nickname=ryuo_nickname)

                # 设置专属称号，并取消前一个人的称号
                self.CQApi.set_group_special_title(self.target_group, ryuo_qq, "今日喷水龙王")
                if last_ryuo:
                    self.CQApi.set_group_special_title(self.target_group, last_ryuo.qq, "")

                # 设置为管理员,并取消前一天的管理员
                AdminUserModel.instance.add_admin(ryuo_qq)
                if last_ryuo:
                    AdminUserModel.instance.remove_admin(last_ryuo.qq)

                # 发到群里
                self.CQApi.send_group_message(self.target_group, None, message)

                self.ev.wait(60)

            else:
                self.ev.wait(60)
