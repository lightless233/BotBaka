#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.ncov
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import json
import re
from typing import List

import requests
from bs4 import BeautifulSoup

from .base import BaseCommand
from BotBaka.utils.log import logger


class NCovCommand(BaseCommand):
    """
    %ncov 浙江
    %ncov list
    %ncov all
    """

    def __init__(self):
        super(NCovCommand, self).__init__()

        self.command_name = "%ncov"

        self.error_msg = "格式错误\n%ncov 浙江 - 显示浙江数据\n%ncov list - 显示所有省份详细信息\n%ncov all - 全国统计信息"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        try:
            province = command_list[1]
        except IndexError:
            self.CQApi.send_group_message(from_group, from_qq, self.error_msg)
            return

        url = "https://3g.dxy.cn/newh5/view/pneumonia"
        response = requests.get(url, timeout=12)
        soup = BeautifulSoup(response.content)
        text = soup.find(id="getAreaStat").text
        pattern = r"window\.getAreaStat = (.+)}catch\(e\){}"
        j = re.search(pattern, text).group(1)
        results = json.loads(j)

        # 全国信息
        global_data = soup.find(class_="content___2hIPS").find_all('span')

        if province == "list":

            message = ""

            for p_data in results:
                province_name = p_data.get("provinceName")
                message += "【{}】\n".format(province_name)
                message += "确认病例：{}\n".format(p_data.get("confirmedCount"))
                message += "治愈病例：{}\n".format(p_data.get("curedCount"))
                message += "死亡病例：{}\n".format(p_data.get("deadCount"))
                message += "=========="
                message += "【{}】中各城市统计数据：\n".format(province_name)
                for city_data in p_data.get("cities"):
                    message += "【{}】确认：{}，治愈：{}，死亡：{}\n".format(
                        city_data.get("cityName"),
                        city_data.get("confirmedCount"),
                        city_data.get("curedCount"),
                        city_data.get("deadCount"),
                    )

            self.CQApi.send_group_message(from_group, from_qq, message)

        elif province == "all":
            stat = []
            for idx, tag_span in enumerate(global_data):
                if idx % 2 == 0:
                    continue

                num = tag_span.text
                stat.append(num)

            message = "【全国统计】\n"
            message += "确诊：{}".format(stat[0])
            message += "疑似：{}".format(stat[1])
            message += "死亡：{}".format(stat[2])
            message += "治愈：{}".format(stat[3])
            self.CQApi.send_group_message(from_group, from_qq, message)

        else:
            for item in results:
                province_name = item.get("provinceName")
                province_short_name = item.get("provinceShortName")
                if province in (province_name, province_short_name):
                    message = "【{}】\n".format(province_name)
                    message += "确认病例：{}\n".format(item.get("confirmedCount"))
                    message += "治愈病例：{}\n".format(item.get("curedCount"))
                    message += "死亡病例：{}\n".format(item.get("deadCount"))
                    message += "=========="
                    message += "【{}】中各城市统计数据：\n".format(province_name)
                    for city_data in item.get("cities"):
                        message += "【{}】确认：{}，治愈：{}，死亡：{}\n".format(
                            city_data.get("cityName"),
                            city_data.get("confirmedCount"),
                            city_data.get("curedCount"),
                            city_data.get("deadCount"),
                        )

                    self.CQApi.send_group_message(from_group, from_qq, message)
