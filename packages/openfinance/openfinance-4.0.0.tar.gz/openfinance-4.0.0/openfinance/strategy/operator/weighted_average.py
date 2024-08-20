import numpy as np

from openfinance.config.macro import MLOG
from openfinance.strategy.operator.base import Operator

class WeightAverage(Operator):
    name:str = "WeightAverage"

    def run(
        self,
        data,
        **kwargs
    ):
        """
            获取权重加强均值 a[0] weight, a[1] value
        """
        MLOG.debug(f"data: {data}")
        reverse = kwargs.get("reverse", True)
        value = 0
        total = 0
        for a in data:
            if a[0] and a[1]: # delete error value
                total += a[0]
                if reverse:
                    value += a[0]/a[1]
                else:
                    value += a[0] * a[1]
        MLOG.debug(f"total: {total}, value: {value}")
        return total / (value + 0.000001)