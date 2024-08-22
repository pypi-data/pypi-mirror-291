# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     voice.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/22
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class VoicePathAndroidSuffix(Enum):
    window_list = '/voice/listWindow'
    entrance = '/voice/entrance'


class VoicePathIOSSuffix(Enum):
    pass


class VoiceHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_voice_window_list(self, json: dict) -> dict:
        """获取连麦窗口列表"""
        return self.http_client.send_request(method="post", path=VoicePathAndroidSuffix.window_list.value, json=json)

    def get_voice_entrance(self, json: dict) -> dict:
        """获取连麦入口配置"""
        return self.http_client.send_request(method="post", path=VoicePathAndroidSuffix.entrance.value, json=json)
