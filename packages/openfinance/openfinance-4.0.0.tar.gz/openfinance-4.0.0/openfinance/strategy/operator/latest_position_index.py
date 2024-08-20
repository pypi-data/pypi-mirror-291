import numpy as np

from openfinance.strategy.operator.base import Operator


NO_DIVIDENT = -100000

class LatestPosition(Operator):
    name:str = "LatestPosition"

    def run(
        self,
        data,
        **kwargs
    ):
        """
            获取最新的指标在一段窗口期间的排序位置
        """
        latest = kwargs.get("latest", True)
        # print("data: ", data)
        if isinstance(data, list): # db select format
            window = kwargs.get("window", len(data))
            assert len(data) > window, f"data is shorter than {window}"
            window -= 1 # delete self
            result = [1] * (len(data) - window)
            for i in range(window, len(data)):
                last = data[i]
                for d in data[i-window:i]:
                    if d > last:
                        result[i-window] += 1
            if latest:
                return result[-1]
            else:
                return result
        return 