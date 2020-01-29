#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.timer.ncov
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
import json
import re

import requests
from bs4 import BeautifulSoup

from .engine.thread import SingleThreadEngine
from ..database.models import NewsModel
from ..utils.log import logger


class NcovTimer(SingleThreadEngine):

    def __init__(self):
        super(NcovTimer, self).__init__()

        self.url = "https://3g.dxy.cn/newh5/view/pneumonia"

        self.name = "ncov-timer"

    def _worker(self):

        logger.info("ncov-timer start!")

        while self.is_running():

            self.ev.wait(60 * 5)

            response = requests.get(self.url, timeout=12)
            soup = BeautifulSoup(response.content)
            data = soup.find(id="getTimelineService").text
            pattern = r"window\.getTimelineService\s*=\s*(.+)}catch\(e\){}"
            j = re.search(pattern, data)
            data = json.loads(j)

            for d in data:
                title = "【{}】【{}】{}\n{}".format(d.get("id"), d.get("infoSource"), d.get("title"), d.get("summary"))
                link = d.get("sourceUrl")
                NewsModel.instance.create(title=title, url=link, has_send=1)
