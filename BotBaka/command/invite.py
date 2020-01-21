#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.attack
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import datetime
import time
from typing import List

from .base import BaseCommand
from ..database.models import AppointmentModel, AppointmentUserModel
from ..utils.quick_at import QuickAt


class InviteCommand(BaseCommand):
    """

    %invite 文明6 2020-01-21/21:00 @a @b @c
    活动结束前15分钟，如果没有拒绝，默认为接受状态
    预约时间必须大于半小时
    """

    def __init__(self):
        super(InviteCommand, self).__init__()

        self.command_name = "%invite"

        self.err_msg = "格式错误。格式：%invite 文明6 2020-01-01/12:00 @userA @UserB ..."

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        try:
            event_name = command_list[1]
            event_time = command_list[2]
            users = command_list[3:]
        except IndexError:
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        if len(users) == 0:
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return

        # parse 预约时间
        try:
            event_time = datetime.datetime.strptime(event_time, "%Y-%m-%d/%H:%M")
        except ValueError:
            self.CQApi.send_group_message(from_group, from_qq, "时间格式错误，请使用：%Y-%m-%d_%H:%M:%S格式")
            return

        # 检查预约时间和当前时间，预约时间必须大于半小时
        if time.mktime(event_time.timetuple()) - time.time() < 60 * 30:
            self.CQApi.send_group_message(from_group, from_qq, "预约时间必须大于当前半小时及以上。")
            return

        # 把预约的事件存起来
        _obj = AppointmentModel.instance.create(
            event_name=event_name,
            event_time=event_time,
            has_end=0,
            organizer=from_qq,
        )

        # 把预约的用户存起来
        qqs = []
        for user in users:
            user_qq = QuickAt.get_qq_from_at_msg(user)
            if not user_qq:
                self.CQApi.send_group_message(from_group, from_qq, "目标用户有误。")
                return
            qqs.append(user_qq)

        for qq in qqs:
            AppointmentUserModel.instance.create(
                event_id=_obj.id,
                user_id=qq,
                accepted=-1,
                gu=-1,
            )

        msg = "邀请成功，请以下用户尽快确认，事件id：{}, " \
              "如果违约将要变成鸽子精哦~\n".format(_obj.id) + ", ".join(
            [QuickAt.build_at_msg(qq) for qq in qqs]
        )
        self.CQApi.send_group_message(from_group, from_qq, msg)


class InviteAcceptCommand(BaseCommand):
    """
    确认是否接受邀请的命令
    %invite_accept event_id true/false
    %ia event_id true/false
    """

    def __init__(self):
        super(InviteAcceptCommand, self).__init__()

        self.command_name = "invite_accept"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        try:
            event_id = command_list[1]
            action = command_list[2]
        except IndexError:
            self.CQApi.send_group_message(
                from_group, from_qq,
                "格式有误，格式：%invite_accept event_id true/false"
            )
            return

        # 检查 event 是否已经结束了，如果结束了不能再处理了
        event_obj = AppointmentModel.instance.get_event_by_id(event_id)
        if event_obj is None or event_obj.has_end == 1:
            self.CQApi.send_group_message(
                from_group, from_qq,
                "该活动不存在或已结束！"
            )
            return

        # 如果不是这个event的邀请人
        is_invited = False
        user_obj: AppointmentUserModel = None
        invited_users = AppointmentUserModel.instance.get_invited_user_by_id(event_obj.id)
        for iu in invited_users:
            if iu.user_id == from_qq:
                is_invited = True
                user_obj = iu
                break
        if not is_invited:
            self.CQApi.send_group_message(from_group, from_qq, "你没有被邀请参加该活动哦，请直接联系活动主办方参加！")
            return

        action = action.lower()
        if action == "false" or action == "f":
            accepted = 0
        elif action == "true" or action == "t":
            accepted = 1
        else:
            self.CQApi.send_group_message(from_group, from_qq, "你说的什么玩意？")
            return

        user_obj.accepted = accepted
        user_obj.gu = 0
        user_obj.save()
        self.CQApi.send_group_message(from_group, from_qq, "处理成功！")


class InviteGuCommand(BaseCommand):
    """
    活动主办方可以使用，来决定谁有没有咕咕咕
    %invite_gu event_id @user
    %ig event_id @user
    """

    def __init__(self):
        super(InviteGuCommand, self).__init__()
        self.command_name = "%invite_gu"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        try:
            event_id = command_list[1]
            user_id = command_list[2]
        except IndexError:
            self.CQApi.send_group_message(from_group, from_qq, "格式错误。格式：%invite_gu event_id @user")
            return

        # 检查 event 是否已经结束了，如果还没有结束，不能设置咕咕咕
        event_obj = AppointmentModel.instance.get_event_by_id(event_id)
        if event_obj is None or event_obj.has_end == 0:
            self.CQApi.send_group_message(
                from_group, from_qq,
                "该活动不存在或未结束！"
            )
            return

        if event_obj.organizer != from_qq:
            self.CQApi.send_group_message(from_group, from_qq, "你不是这个活动的发起人！")
            return

        # 检查目标用户是否是这个活动的邀请人
        user_id = QuickAt.get_qq_from_at_msg(user_id)
        if user_id is None:
            self.CQApi.send_group_message(from_group, from_qq, "1-我都懒得写错误信息了，你自己看吧!")
            return

        invited_users = AppointmentUserModel.instance.get_invited_user_by_id(event_id)
        invited_user_ids = [iu.user_id for iu in invited_users]
        if user_id not in invited_user_ids:
            self.CQApi.send_group_message(from_group, from_qq, "目标用户没有被邀请!")
            return

        # 获取目标用户obj
        user_obj = AppointmentUserModel.instance.get_user(event_id, user_id)
        if user_obj is None:
            self.CQApi.send_group_message(from_group, from_qq, "2-我都懒得写错误信息了，你自己看吧!")
            return

        user_obj.gu = 1
        user_obj.title_end_time = datetime.datetime.now() + datetime.timedelta(hours=12)
        user_obj.save()

        # 设置title
        self.CQApi.set_group_special_title(from_group, from_qq, "鸽子精咕咕咕")
        self.CQApi.send_group_message(from_group, from_qq, "设置咕咕咕成功！")
