#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    BotBaka.command.weather
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    $END$

    :author:    lightless <root@lightless.me>
    :homepage:  None
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017-2020 lightless. All rights reserved
"""
from typing import List

import requests
from django.conf import settings

from .base import BaseCommand


class WeatherCommand(BaseCommand):

    def __init__(self):
        super(WeatherCommand, self).__init__()
        self.command_name = "%weather"

        self.weather_now_api = "https://free-api.heweather.net/s6/weather/now"
        self.weather_forecast_api = "https://free-api.heweather.net/s6/weather/forecast"
        self.air_now_api = "https://free-api.heweather.net/s6/air/now"

        self.api_key = settings.WEATHER_KEY

        self.error_msg = "参数错误\n%weather 杭州/hanghzou"

    def process(self, from_group: int, from_qq: int, name: str, command_list: List[str]):

        is_detail = False
        command = command_list[0]
        if command == "weather-detail":
            is_detail = True
        else:
            is_detail = False

        try:
            city = command_list[1]
        except IndexError:
            self.CQApi.send_group_message(from_group, from_qq, self.error_msg)
            return

        params = {
            "key": self.api_key,
            "location": city,
        }

        # 先获取now的数据，然后获取预报数据，然后获取空气质量数据，最后组装

        # 实况数据
        response = requests.get(self.weather_now_api, params=params, timeout=9)
        now_weather_result = response.json().get("HeWeather6")[0]
        now_city = now_weather_result.get("basic")
        now_weather = now_weather_result.get("now")

        # 如果没有请求详细数据，可以返回了
        base_message = "[天气预报小助手]\n"
        base_message += "{} 当前天气 {}\n".format(now_city.get("location"), now_weather.get("cond_txt"))
        base_message += "温度：{}摄氏度, 体感温度：{}摄氏度\n".format(now_weather.get("tmp"), now_weather.get("fl"))
        base_message += "{}，{}级，风速：{}km/h\n".format(now_weather.get("wind_dir"), now_weather.get("wind_sc"),
                                                    now_weather.get("wind_spd"))
        base_message += "相对湿度：{}，降水量：{}\n".format(now_weather.get("hum"), now_weather.get("pcpn"))
        base_message += "大气压强：{}，能见度：{}，云量：{}".format(
            now_weather.get("pres"), now_weather.get("vis"), now_weather.get("cloud")
        )

        if not is_detail:
            base_message += "当期在使用免费的API接口，赞助我一杯咖啡钱，可以切换到收费API获取更多功能哦~"
            self.CQApi.send_group_message(from_group, from_qq, base_message)
        else:
            # 请求详细数据，需要获取更多的信息
            forecast_message = "【未来天气预报】"
            forecast_response = requests.get(self.weather_forecast_api, params=params, timeout=9)
            forecast_response = forecast_response.json()
            daily_forecast = forecast_response.get("HeWeather6")[0].get("daily_forecast")
            for daily_weather in daily_forecast:
                date = daily_weather.get("date")
                forecast_message += "{}天气信息：\n".format(date)
                forecast_message += "气温：{}-{}摄氏度\n".format(daily_weather.get("tmp_min"), daily_weather.get("tmp_max"))
                forecast_message += "{}转{}，降水概率：{}\n".format(
                    daily_weather.get("cond_txt_d"),
                    daily_weather.get("cond_txt_n"),
                    daily_weather.get("pop")
                )
                forecast_message += "{}，{}级\n".format(daily_weather.get("wind_dir"), daily_weather.get("wind_sc"))
                forecast_message += "相对湿度：{}，降水量：{}，大气压强：{}，紫外线强度：{}\n".format(
                    daily_weather.get("hum"), daily_weather.get("pcpn"), daily_weather.get("pres"),
                    daily_weather.get("uv_index")
                )
                forecast_message += "日出：{}，日落：{}，月出：{}，月落：{}\n"
                forecast_message += "=========\n\n"

            air_response = requests.get(self.air_now_api, params=params, timeout=9)
            air_response = air_response.json()
            air_message = "【空气质量】\n"
            air_now_city = air_response.get("HeWeather6")[0].get("air_now_city")
            air_now_station = air_response.get("HeWeather6")[0].get("air_now_station")
            air_message += "空气质量：{}，首要污染物：{}\n".format(air_now_city.get("qlty"), air_now_city.get("main"))
            air_message += "AQI: {}, PM2.5: {}, PM10: {}, NO2: {}, SO2: {}, CO: {}, O3: {}\n".format(
                air_now_city.get("aqi"),
                air_now_city.get("pm25"),
                air_now_city.get("pm10"),
                air_now_city.get("no2"),
                air_now_city.get("so2"),
                air_now_city.get("co"),
                air_now_city.get("o3"),
            )
            air_message += "更新时间：{}\n".format(air_now_city.get("pub_time"))
            air_message += "==========\n"
            for _station in air_now_station:
                air_message += "{}, 首要污染物: {}, 空气质量: {}\n".format(
                    _station.get("air_sta"), _station.get("main"), _station.get("qlty")
                )
                air_message += "AQI: {}, PM2.5: {}, PM10: {}, NO2: {}, SO2: {}, CO: {}, O3: {}\n".format(
                    _station.get("aqi"),
                    _station.get("pm25"),
                    _station.get("pm10"),
                    _station.get("no2"),
                    _station.get("so2"),
                    _station.get("co"),
                    _station.get("o3"),
                )
                air_message += "==========\n"

            base_message += forecast_message + "\n" + air_message + "\n"
            base_message += "当期在使用免费的API接口，赞助我一杯咖啡钱，可以切换到收费API获取更多功能哦~"
            self.CQApi.send_group_message(from_group, from_qq, base_message)
