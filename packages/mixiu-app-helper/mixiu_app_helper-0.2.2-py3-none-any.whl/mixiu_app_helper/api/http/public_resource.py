# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     public_resource.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class PublicResourcePathAndroidSuffix(Enum):
    level_relation_list = '/pr/levelRelation/list'


class PublicResourcePathIOSSuffix(Enum):
    pass


class PublicResourceHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_pr_level_relation_list(self, json: dict) -> dict:
        """获取用户的层级关系列表"""
        return self.http_client.send_request(
            method="post", path=PublicResourcePathAndroidSuffix.level_relation_list.value, json=json
        )
