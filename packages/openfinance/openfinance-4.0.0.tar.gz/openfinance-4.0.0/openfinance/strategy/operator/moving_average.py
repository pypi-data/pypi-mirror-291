import numpy as np
from talib.abstract import *
from openfinance.strategy.operator.base import Operator

class MovingAverage(Operator):
    name: str = "MovingAverage"

    def run(
        self,
        data,
        **kwargs
    ):
        """
            获取移动平均值
        """
        
        window = kwargs.get("window", 5)
        latest = kwargs.get("latest", True)

        # result = 0
        # #print(data)
        # slope = np.convolve(
        #     np.array(data, dtype='double'), np.ones(window), "valid") / window
        # # print(",".join(map(str, slope)))
        # # Or 
        slope = SMA(np.array(data, dtype='double'), window)
        if latest:
            return slope[-1]
        return slope