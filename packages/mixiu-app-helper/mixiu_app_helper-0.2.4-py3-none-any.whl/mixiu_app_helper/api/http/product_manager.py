# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     product_manager.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class ProductManagerPathAndroidSuffix(Enum):
    advertisement_index_list = '/pm/indexAdvertisement'
    app_styles = '/pm/appStyles'


class ProductManagerPathIOSSuffix(Enum):
    pass


class ProductManagerHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_pm_advertisement_index_list(self, json: dict) -> dict:
        """获取宣传广告索引"""
        return self.http_client.send_request(
            method="post", path=ProductManagerPathAndroidSuffix.advertisement_index_list.value, json=json
        )

    def get_pm_app_styles(self, json: dict) -> dict:
        """获取app样式风格"""
        return self.http_client.send_request(
            method="post", path=ProductManagerPathAndroidSuffix.app_styles.value, json=json
        )
