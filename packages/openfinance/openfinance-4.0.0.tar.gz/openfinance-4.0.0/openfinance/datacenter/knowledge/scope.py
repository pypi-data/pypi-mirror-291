# -*- coding: utf-8 -*-
# (C) Run, Inc. 2022
# All rights reserved (Author BinZHU)
# Licensed under Simplified BSD License (see LICENSE)
# @Desc: { 尺度枚举类模块 }

from enum import Enum

class ScopeCodeEnum(Enum):
    """状态码枚举类"""

    DAY = ("DAY", '天')
    WEEK = ("WEEK", '周')
    MONTH = ("MONTH", '月')
    YEAR = ("YEAR", '年')

    @property
    def code(self):
        """获取状态码"""
        return self.value[0]

    @property
    def zh(self):
        """获取中文"""
        return self.value[1]

class RangeEnum(Enum):
    """区间长度枚举"""

    R1 = 1
    R5 = 5
    R10 = 10
    R60 = 60
    R120 = 120

    @property
    def code(self):
        """获取状态码"""
        return self.value