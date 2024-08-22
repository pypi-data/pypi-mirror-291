# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     auth.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/12
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class AuthPathAndroidSuffix(Enum):
    auth_info = '/auth/getAuthInfos'


class AuthPathIOSSuffix(Enum):
    pass


class AuthHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_auth_info(self, json: dict) -> dict:
        """获取认证信息"""
        return self.http_client.send_request(method="post", path=AuthPathAndroidSuffix.auth_info.value, json=json)
