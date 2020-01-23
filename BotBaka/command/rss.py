#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.rss
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from typing import List

from .base import BaseCommand
from ..database.models import RssSourceModel


class RssCommand(BaseCommand):
    """
    %rss add/delete name rss_link
    %rss add oss-sec https://seclists.org/rss/oss-sec.rss
    %rss delete oss-sec
    %rss list
    """

    def __init__(self):
        super(RssCommand, self).__init__()

        self.command_name = "%rss"

        self.err_msg = "参数有误。格式：\n%rss add/delete name rss_link\n%rss add oss-sec https://seclists.org/rss/oss-sec.rss"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):
        try:
            action = command_list[1]
            name = command_list[2]
            # rss_link = command_list[3]
        except IndexError:
            self.CQApi.send_group_message(
                from_group, from_qq,
                self.err_msg
            )
            return

        action = action.lower()
        if action == "add":
            try:
                rss_link = command_list[3]
            except IndexError:
                self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
                return

            # 检查这个rss link是否已经存在了
            obj = RssSourceModel.instance.get_by_url(rss_link)
            if obj:
                self.CQApi.send_group_message(from_group, from_qq, "该RSS源已存在")
                return
            else:
                if RssSourceModel.instance.create(name=name, url=rss_link):
                    self.CQApi.send_group_message(from_group, from_qq, "操作成功!")
                    return
                else:
                    self.CQApi.send_group_message(from_group, from_qq, "操作失败!")
                    return
        elif action in ("remove", "delete", "del"):
            RssSourceModel.instance.filter(name=name).delete()
            self.CQApi.send_group_message(from_group, from_qq, "删除成功!")
            return
        elif action == "list":
            all_sources = RssSourceModel.instance.all()
            msg = "[RSS LIST]\n"
            for s in all_sources:
                msg += "{} - {}\n".format(s.name, s.url)
            self.CQApi.send_group_message(from_group, from_qq, msg)
        else:
            self.CQApi.send_group_message(from_group, from_qq, self.err_msg)
            return
