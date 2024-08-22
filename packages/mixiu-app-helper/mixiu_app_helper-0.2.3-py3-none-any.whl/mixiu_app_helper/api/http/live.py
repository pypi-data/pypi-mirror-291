# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     live.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class LivePathAndroidSuffix(Enum):
    category_list = '/live/category/list'
    pre_load_resource = '/l/pre/load/live/resource'


class LivePathIOSSuffix(Enum):
    pass


class LiveHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_live_category_list(self, json: dict) -> dict:
        """获取直播类目列表"""
        return self.http_client.send_request(method="post", path=LivePathAndroidSuffix.category_list.value, json=json)

    def get_pre_load_resource(self, json: dict) -> dict:
        """获取直播预加载资源"""
        return self.http_client.send_request(
            method="post", path=LivePathAndroidSuffix.pre_load_resource.value, json=json
        )
