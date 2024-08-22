# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     relation.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/22
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class RelationPathAndroidSuffix(Enum):
    friend_recommend = '/relation/friend/recommend'


class RelationPathIOSSuffix(Enum):
    pass


class RelationHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_relation_friend_recommend(self, json: dict) -> dict:
        """获取登录人朋友推荐信息"""
        return self.http_client.send_request(
            method="post", path=RelationPathAndroidSuffix.friend_recommend.value, json=json
        )
