# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     resource.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class ResourcePathAndroidSuffix(Enum):
    video_list = '/res/webp'


class ResourcePathIOSSuffix(Enum):
    pass


class ResourceHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_video_list(self, json: dict) -> dict:
        """获取视频资源"""
        return self.http_client.send_request(method="post", path=ResourcePathAndroidSuffix.video_list.value, json=json)
