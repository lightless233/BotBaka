#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.timer.invite
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import datetime

from BotBaka.database.models import AppointmentModel, AppointmentUserModel
from BotBaka.timer.engine.thread import SingleThreadEngine
from BotBaka.utils.log import logger


class InviteTimer(SingleThreadEngine):

    def __init__(self):
        super(InviteTimer, self).__init__()

        self.name = "invite-timer"

        self.target_group = 672534169

    def _worker(self):

        logger.debug("{} start!".format(self.name))

        while self.is_running():
            # 获取所有的未完成活动
            active_events = AppointmentModel.instance.get_all_active_event()
            now = datetime.datetime.now()

            for _event in active_events:
                # 看看有没有已经完成的活动
                if now > _event.event_time:
                    _event.has_end = True
                    _event.save()
                    logger.debug("更新活动{}-{}为完成状态".format(_event.event_name, _event.id))

                # 看看有没有 5 分钟到期的活动
                # 如果距离活动开始5分钟，还有人没有确认，自动设置为咕咕咕
                if _event.event_time - datetime.timedelta(minutes=5) < now:
                    invited_users = AppointmentUserModel.instance.get_invited_user_by_id(_event.id)
                    for iu in invited_users:
                        if iu.accepted == -1 and iu.gu == -1:
                            iu.gu = 1
                            iu.title_end_time = datetime.datetime.now() + datetime.timedelta(hours=12)
                            iu.save()
                            self.CQApi.set_group_special_title(self.target_group, iu.user_id, "鸽子精咕咕咕")
                            logger.info("标记{}为鸽子精".format(iu.user_id))

            # 取消到期的title
            un_process_users = AppointmentUserModel.instance.get_gu_user()
            for _user in un_process_users:
                if _user.title_end_time < now:
                    # 取消title
                    self.CQApi.set_group_special_title(self.target_group, _user.user_id, "")
                    _user.has_title = 1
                    _user.save()
                    logger.debug("取消{}的鸽子精称号！".format(_user))

            self.ev.wait(60)
