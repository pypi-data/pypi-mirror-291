import numpy as np

from openfinance.strategy.operator.base import Operator


NO_DIVIDENT = -100000

class DivideLatest(Operator):
    name:str = "DivideLatest"

    def run(
        self,
        data,
        **kwargs
    ):
        """
            获取最新的两个值的比值
        """
        # print("DivideLatest data: ", data)
        try:
            latestdata = data[-1]
            if not isinstance(latestdata, list):
                latestdata = data
            if len(latestdata) == 2:
                if latestdata[0]:
                    return latestdata[1]/latestdata[0]
                else:
                    return - latestdata[1] * NO_DIVIDENT
        except:
            print(data)
        return NO_DIVIDENT