# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  mixiu-app-helper
# FileName:     portal.py
# Description:  TODO
# Author:       zhouhanlin
# CreateDate:   2024/08/16
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from poco.proxy import UIObjectProxy
from airtest_helper.core import DeviceApi
from airtest_helper.platform import ANDROID_PLATFORM
from airtest_helper.libs.extend import get_poco_factory


class UiMyPortalApi(DeviceApi):

    def get_my(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/tvTabItemText4"
        options = dict(d_type=d_type, name=name, text="我的")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_my(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> bool:
        my_poco = self.get_my(loop=loop, peroid=peroid, **kwargs)
        if my_poco:
            my_poco.click()
            return True
        return False


class UiHomePortalApi(DeviceApi):

    def get_home(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/tvTabItemText1"
        options = dict(d_type=d_type, name=name, text="首页")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_home(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> bool:
        my_poco = self.get_home(loop=loop, peroid=peroid, **kwargs)
        if my_poco:
            my_poco.click()
            return True
        return False


class UiSquarePortalApi(DeviceApi):

    def get_square(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/tvTabItemText2"
        options = dict(d_type=d_type, name=name, text="广场")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_square(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> bool:
        my_poco = self.get_square(loop=loop, peroid=peroid, **kwargs)
        if my_poco:
            my_poco.click()
            return True
        return False


class UiMessagePortalApi(DeviceApi):

    def get_message(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> UIObjectProxy:
        d_type = ""
        name = ""
        if self.platform == ANDROID_PLATFORM:
            d_type = "android.widget.TextView"
            name = "com.mixiu.com:id/tvTabItemText3"
        options = dict(d_type=d_type, name=name, text="消息")
        return get_poco_factory(poco=self.poco, options=options, loop=loop, peroid=peroid, **kwargs)

    def touch_message(self, loop: int = 20, peroid: float = 0.5, **kwargs) -> bool:
        my_poco = self.get_message(loop=loop, peroid=peroid, **kwargs)
        if my_poco:
            my_poco.click()
            return True
        return False
