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
    share_info = '/room/share/getShareInfo'
    web_resource_menu = '/room/resource/listWebRoomResourceMenu'
    resource_menu = '/room/resource/listRoomResourceMenu'
    user_seat_info = '/room/getSeatUserInfo'
    entry = '/room/entry'


class RoomPathIOSSuffix(Enum):
    pass


class RoomHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_room_rookie_recommend_list(self, json: dict) -> dict:
        """获取语音房新手推荐"""
        return self.http_client.send_request(
            method="post", path=RoomPathAndroidSuffix.rookie_recommend_list.value, json=json
        )

    def get_room_quick_entrance_label_list(self, json: dict) -> dict:
        """获取语音房快速入口标签列表"""
        return self.http_client.send_request(
            method="post", path=RoomPathAndroidSuffix.quick_entrance_label_list.value, json=json
        )

    def get_room_hot_recommend_list(self, json: dict) -> dict:
        """获取语音房热门推荐列表"""
        return self.http_client.send_request(
            method="post", path=RoomPathAndroidSuffix.hot_recommend_list.value, json=json
        )

    def get_room_catalogue_list(self, json: dict) -> dict:
        """获取语音房catalogue配置"""
        return self.http_client.send_request(
            method="post", path=RoomPathAndroidSuffix.room_catalogue_list.value, json=json
        )

    def get_room_share_info(self, json: dict) -> dict:
        """获取语音房的共享信息"""
        return self.http_client.send_request(method="post", path=RoomPathAndroidSuffix.share_info.value, json=json)

    def get_room_web_resource_menu(self, json: dict) -> dict:
        """获取语音房H5资源菜单列表"""
        return self.http_client.send_request(
            method="post", path=RoomPathAndroidSuffix.web_resource_menu.value, json=json
        )

    def get_room_resource_menu(self, json: dict) -> dict:
        """获取语音房资源菜单列表"""
        return self.http_client.send_request(method="post", path=RoomPathAndroidSuffix.resource_menu.value, json=json)

    def get_room_user_seat_info(self, json: dict) -> dict:
        """获取语音房用户座位信息"""
        return self.http_client.send_request(method="post", path=RoomPathAndroidSuffix.user_seat_info.value, json=json)

    def get_room_entry(self, json: dict) -> dict:
        """获取语音房入口信息"""
        return self.http_client.send_request(method="post", path=RoomPathAndroidSuffix.entry.value, json=json)
