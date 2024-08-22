# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     home.py
# Description:  操作入口
# Author:       zhouhanlin
# CreateDate:   2024/08/16
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from poco.proxy import UIObjectProxy
from airtest_helper.platform import ANDROID_PLATFORM
from airtest_helper.libs.extend import get_poco_factory
from mixiu_app_helper.api.page.portal import UiHomePortalApi


class UiHomeApi(UiHomePortalApi):

    def get_room_tab(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.ImageView"
            name = "com.mixiu.com:id/ivRoomTextIcon"
        options = dict(d_type=d_type, name=name)
        poco_factory = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if poco_factory:
            return poco_factory
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/tvRoomText"
        options = dict(d_type=d_type, name=name, text="房间")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_room_tab(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> bool:
        room_enter_poco = self.get_room_tab(loop=loop, peroid=peroid, **kwargs)
        if room_enter_poco:
            room_enter_poco.click()
            return True
        return False

    def get_live_tab(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.ImageView"
            name = "com.mixiu.com:id/ivLiveTextIcon"
        options = dict(d_type=d_type, name=name)
        poco_factory = get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)
        if poco_factory:
            return poco_factory
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/tvLiveText"
        options = dict(d_type=d_type, name=name, text="直播")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_live_tab(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> bool:
        live_enter_poco = self.get_live_tab(loop=loop, peroid=peroid, **kwargs)
        if live_enter_poco:
            live_enter_poco.click()
            return True
        return False

    def __get_hot_tab(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/pagerTitleTv"
        options = dict(d_type=d_type, name=name, text="热门")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def __get_vicinity_tab(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/pagerTitleTv"
        options = dict(d_type=d_type, name=name, text="附近")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def __get_pager_title_icon_iv(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.ImageView"
            name = "com.mixiu.com:id/pagerTitleIconIv"
        options = dict(d_type=d_type, name=name)
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def get_hot_tab(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        vicinity_poco = self.__get_vicinity_tab(loop=loop, peroid=peroid, **kwargs)
        if vicinity_poco:
            return self.__get_pager_title_icon_iv(loop=loop, peroid=peroid, **kwargs)
        else:
            return self.__get_hot_tab(loop=loop, peroid=peroid, **kwargs)

    def touch_hot_tab(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> bool:
        hot_enter_poco = self.get_hot_tab(loop=loop, peroid=peroid, **kwargs)
        if hot_enter_poco:
            hot_enter_poco.click()
            return True
        return False

    def get_vicinity_tab(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        hot_poco = self.__get_hot_tab(loop=loop, peroid=peroid, **kwargs)
        if hot_poco:
            return self.__get_pager_title_icon_iv(loop=loop, peroid=peroid, **kwargs)
        else:
            return self.__get_vicinity_tab(loop=loop, peroid=peroid, **kwargs)

    def touch_vicinity(self, loop: int = 10, peroid: float = 0.5, **kwargs) -> bool:
        vicinity_enter_poco = self.get_vicinity_tab(loop=loop, peroid=peroid, **kwargs)
        if vicinity_enter_poco:
            vicinity_enter_poco.click()
            return True
        return False

    def get_home_search_enter(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.ImageView"
            name = "com.mixiu.com:id/ivHomeTopSearch"
        options = dict(d_type=d_type, name=name)
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_home_search_enter(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> bool:
        search_enter_poco = self.get_home_search_enter(loop=loop, peroid=peroid, **kwargs)
        if search_enter_poco:
            search_enter_poco.click()
            return True
        return False

    def get_home_favorite_enter(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.ImageView"
            name = "com.mixiu.com:id/ivHomeTopHeart"
        options = dict(d_type=d_type, name=name)
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_home_favorite_enter(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> bool:
        favorites_enter_poco = self.get_home_favorite_enter(loop=loop, peroid=peroid, **kwargs)
        if favorites_enter_poco:
            favorites_enter_poco.click()
            return True
        return False

    def get_home_start_live_enter(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.ImageView"
            name = "com.mixiu.com:id/ivStartLivePush"
        options = dict(d_type=d_type, name=name)
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_home_start_live_enter(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> bool:
        start_live_enter_poco = self.get_home_start_live_enter(loop=loop, peroid=peroid, **kwargs)
        if start_live_enter_poco:
            start_live_enter_poco.click()
            return True
        return False
