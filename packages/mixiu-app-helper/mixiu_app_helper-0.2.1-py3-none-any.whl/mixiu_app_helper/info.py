# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     info.py
# Description:  TODO
# Author:       zhouhanlin
# CreateDate:   2024/07/16
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum


class Constant(Enum):
    ANDROID_APP_NAME = "com.mixiu.com"
    iOS_APP_NAME = "iOS"


module_tree = {
    "l1-1": "ui",
    "l1-2": "api",
    "l2-1": "ui.my",
    "l2-2": "ui.home",
    "l2-3": "ui.square",
    "l2-4": "ui.message",
    "l2-5": "ui.favorite",
    "l2-6": "ui.emoji",
    "l3-1": "ui.my.profile",
    "l3-2": "ui.my.settings",
    "l3-3": "ui.favorite.voice",
    "l3-4": "ui.favorite.live",
    "l3-5": "ui.emoji.hall",
    "l3-6": "ui.emoji.private_chat",
    "l3-7": "ui.home.room",
    "l3-8": "ui.home.live",
    "l3-9": "ui.message.hall",
    "l3-10": "ui.message.private_chat",
    "l4-1": "ui.home.room.voice",
    "l4-2": "ui.home.live.video",
}
