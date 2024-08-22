# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     music.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class MusicPathAndroidSuffix(Enum):
    switch_config = '/misc/switch/config'


class MusicPathIOSSuffix(Enum):
    pass


class MusicHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_switch_config(self, json: dict) -> dict:
        """获取music切换配置"""
        return self.http_client.send_request(method="post", path=MusicPathAndroidSuffix.switch_config.value, json=json)
