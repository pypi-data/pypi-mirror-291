# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     tour.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/15
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class TourPathAndroidSuffix(Enum):
    check = '/tour/check'


class TourPathIOSSuffix(Enum):
    pass


class TourHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def tour_check(self, json: dict) -> dict:
        """宣传检查"""
        return self.http_client.send_request(method="post", path=TourPathAndroidSuffix.check.value, json=json)
