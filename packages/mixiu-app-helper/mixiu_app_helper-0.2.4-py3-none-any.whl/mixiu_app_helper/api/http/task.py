# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     task.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/22
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum
from mixiu_app_helper.api.http.http_client import HttpApiMeta


class TaskPathAndroidSuffix(Enum):
    week_entrance = '/week/entrance'


class TaskPathIOSSuffix(Enum):
    pass


class TaskHttpApi(HttpApiMeta):

    def __init__(self, domain: str, protocol: str):
        super().__init__(domain, protocol)

    def get_week_entrance(self, json: dict) -> dict:
        """获取本周任务"""
        return self.http_client.send_request(method="post", path=TaskPathAndroidSuffix.week_entrance.value, json=json)
