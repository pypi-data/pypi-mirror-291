# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     im.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class IMPathAndroidSuffix(Enum):
    url = '/im/get/url'


class IMPathIOSSuffix(Enum):
    pass


class IMHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_url(self) -> dict:
        """获取im的url配置"""
        return self.http_client.send_request(method="get", path=IMPathAndroidSuffix.url.value)
