import numpy as np

from openfinance.strategy.operator.base import Operator

class Hist(Operator):
    name:str = "Hist"

    def run(
        self,
        data,
        **kwargs
    ):
        """
            获取小于一定阈值的分布比值
        """
        latest = kwargs.get("high", True)            
        thresh = kwargs.get("thresh", 1)
        assert len(data) > 0, "data is empty"
        count = 0
        for i in data:
            if i <= thresh:
                count += 1
        return count/len(data)
