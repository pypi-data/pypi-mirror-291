# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     favorite.py
# Description:  TODO
# Author:       zhouhanlin
# CreateDate:   2024/08/16
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from poco.proxy import UIObjectProxy
from airtest_helper.platform import ANDROID_PLATFORM
from airtest_helper.libs.extend import get_poco_factory
from mixiu_app_helper.api.page.home.home import UiHomeApi


class UiRoomFavoriteApi(UiHomeApi):

    def get_favorite_room_by_name(self, room_name: str, loop: int = 20, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/tvName"
        options = dict(d_type=d_type, name=name, text=room_name)
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_favorite_room(self, room_name: str, loop: int = 20, peroid: float = 0.5, **kwargs) -> bool:
        room_poco = self.get_favorite_room_by_name(room_name=room_name, loop=loop, peroid=peroid, **kwargs)
        if room_poco:
            room_poco.click()
            return True
        return False


class UiLiveFavoriteApi(UiHomeApi):
    pass
