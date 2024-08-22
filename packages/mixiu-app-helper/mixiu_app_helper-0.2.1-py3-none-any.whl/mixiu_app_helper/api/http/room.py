# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     room.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class RoomPathAndroidSuffix(Enum):
    rookie_recommend_list = '/room/main/listRookieRecommend'
    quick_entrance_label_list = '/room/main/listQuickEntranceLabel'
    hot_recommend_list = '/room/main/listHotRecommend'
    room_catalogue_list = '/room/main/config/v3'


class RoomPathIOSSuffix(Enum):
    pass


class RoomHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_main_rookie_recommend_list(self, json: dict) -> dict:
        """获取语音房新手推荐"""
        return self.http_client.send_request(
            method="post", path=RoomPathAndroidSuffix.rookie_recommend_list.value, json=json
        )

    def get_main_quick_entrance_label_list(self, json: dict) -> dict:
        """获取语音房快速入口标签列表"""
        return self.http_client.send_request(
            method="post", path=RoomPathAndroidSuffix.quick_entrance_label_list.value, json=json
        )

    def get_main_hot_recommend_list(self, json: dict) -> dict:
        """获取语音房热门推荐列表"""
        return self.http_client.send_request(
            method="post", path=RoomPathAndroidSuffix.hot_recommend_list.value, json=json
        )

    def get_main_catalogue_list(self, json: dict) -> dict:
        """获取语音房catalogue配置"""
        return self.http_client.send_request(
            method="post", path=RoomPathAndroidSuffix.room_catalogue_list.value, json=json
        )
