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

        self.url = "https://3g.dxy.cn/newh5/view/pneumonia"

    def __get_bs(self):
        response = requests.get(self.url, timeout=12)
        soup = BeautifulSoup(response.content)
        return soup

    def __get_area_stat(self, soup):
        text = soup.find(id="getAreaStat").text
        pattern = r"window\.getAreaStat = (.+)}catch\(e\){}"
        json_data = re.search(pattern, text).group(1)
        json_data = json.loads(json_data)
        return json_data

    def __get_global_stat(self, soup):
        data = soup.find(id='getStatisticsService').text
        pattern = r"window\.getStatisticsService\s*=\s*(.+)}catch\(e\){}"
        j = re.search(pattern, data).group(1)
        j_data = json.loads(j)
        return j_data

    def __get_timeline(self, soup):
        data = soup.find(id="getTimelineService").text
        pattern = r"window\.getTimelineService\s*=\s*(.+)}catch\(e\){}"
        j = re.search(pattern, data)
        return json.loads(j)

    def __format_item(self, item):
        province_name = item.get("provinceName")

        message = "【{}】\n".format(province_name)
        message += "确认病例：{}\n".format(item.get("confirmedCount"))
        message += "治愈病例：{}\n".format(item.get("curedCount"))
        message += "死亡病例：{}\n".format(item.get("deadCount"))
        message += "==========\n"
        message += "【{}】中各城市统计数据：\n".format(province_name)
        for city_data in item.get("cities"):
            message += "【{}】确认：{}，治愈：{}，死亡：{}\n".format(
                city_data.get("cityName"),
                city_data.get("confirmedCount"),
                city_data.get("curedCount"),
                city_data.get("deadCount"),
            )

        return message

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        try:
            province = command_list[1]
        except IndexError:
            self.CQApi.send_group_message(from_group, from_qq, self.error_msg)
            return

        soup = self.__get_bs()

        if province == "list":
            results = self.__get_area_stat(soup)
            message = ""
            for p_data in results:
                message += self.__format_item(p_data) + "\n"

            self.CQApi.send_group_message(from_group, from_qq, message)
        elif province == "all":
            j_data = self.__get_global_stat(soup)

            message = "【全国统计】\n"
            message += "确诊：{}\n".format(j_data.get("confirmedCount"))
            message += "疑似：{}\n".format(j_data.get("suspectedCount"))
            message += "死亡：{}\n".format(j_data.get("deadCount"))
            message += "治愈：{}\n".format(j_data.get("curedCount"))

            self.CQApi.send_group_message(from_group, from_qq, message)
        else:

            results = self.__get_area_stat(soup)

            for item in results:
                province_name = item.get("provinceName")
                province_short_name = item.get("provinceShortName")
                if province in (province_name, province_short_name):
                    message = self.__format_item(item)
                    self.CQApi.send_group_message(from_group, from_qq, message)
                    return
