# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  catlive-app-helper
# FileName:     info.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/08/19
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from enum import Enum


class Constant(Enum):
    ANDROID_APP_NAME = "com.catlive.app"
    iOS_APP_NAME = "iOS"


module_tree = {
    "l1-1": "ui",
    "l1-2": "api",
    "l2-1": "ui.my",
    "l2-2": "ui.live",
    "l2-3": "ui.room",
    "l2-4": "ui.square",
    "l2-5": "ui.message",
    "l2-6": "ui.favorite",
    "l2-7": "ui.emoji",
    "l3-1": "ui.my.profile",
    "l3-2": "ui.my.settings",
    "l3-3": "ui.favorite.voice",
    "l3-4": "ui.favorite.live",
    "l3-5": "ui.emoji.hall",
    "l3-6": "ui.emoji.private_chat",
    "l3-9": "ui.message.hall",
    "l3-10": "ui.message.private_chat"
}
