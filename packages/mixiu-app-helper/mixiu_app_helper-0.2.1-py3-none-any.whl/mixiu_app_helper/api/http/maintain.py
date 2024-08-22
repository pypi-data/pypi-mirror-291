# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     maintain.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class MaintainPathAndroidSuffix(Enum):
    window_list = '/main/window/list'
    rank_list = '/main/rank'
    misc_default_tab = '/main/misc/defaultTab'
    launch_page = '/main/getLaunchPage'
    event_trigger = '/main/event/trigger'
    distance_list = '/main/distance'
    config_url = '/main/configURL'
    hot_list = '/m/list/hot/v2'
    app_skin = '/m/getAppSkin'
    banner_list_module = '/m/banner/list/module'


class MaintainPathIOSSuffix(Enum):
    pass


class MaintainHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_main_window_list(self, json: dict) -> dict:
        """获取窗口列表"""
        return self.http_client.send_request(method="post", path=MaintainPathAndroidSuffix.window_list.value, json=json)

    def get_main_rank_list(self, json: dict) -> dict:
        """获取风险信息"""
        return self.http_client.send_request(method="post", path=MaintainPathAndroidSuffix.rank_list.value, json=json)

    def get_main_misc_default_tab(self, json: dict) -> dict:
        """获取misc的默认tab"""
        return self.http_client.send_request(
            method="post", path=MaintainPathAndroidSuffix.misc_default_tab.value, json=json
        )

    def get_main_launch_page(self, json: dict) -> dict:
        """获取启动页面"""
        return self.http_client.send_request(method="post", path=MaintainPathAndroidSuffix.launch_page.value, json=json)

    def get_main_event_trigger(self, json: dict) -> dict:
        """获取事件触发器"""
        return self.http_client.send_request(
            method="post", path=MaintainPathAndroidSuffix.event_trigger.value, json=json
        )

    def get_main_distance_list(self, json: dict) -> dict:
        """获取附近资源"""
        return self.http_client.send_request(
            method="post", path=MaintainPathAndroidSuffix.distance_list.value, json=json
        )

    def get_main_config_url(self, json: dict) -> dict:
        """获取配置URL"""
        return self.http_client.send_request(method="post", path=MaintainPathAndroidSuffix.config_url.value, json=json)

    def get_main_hot_list(self, json: dict) -> dict:
        """获取系统热点配置列表"""
        return self.http_client.send_request(method="post", path=MaintainPathAndroidSuffix.hot_list.value, json=json)

    def get_main_app_skin(self, json: dict) -> dict:
        """获取app皮肤"""
        return self.http_client.send_request(method="post", path=MaintainPathAndroidSuffix.app_skin.value, json=json)

    def get_main_banner_list_module(self, json: dict) -> dict:
        """获取首页banner列表模块"""
        return self.http_client.send_request(
            method="post", path=MaintainPathAndroidSuffix.banner_list_module.value, json=json
        )
