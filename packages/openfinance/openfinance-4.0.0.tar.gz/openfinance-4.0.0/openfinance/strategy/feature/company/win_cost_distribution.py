import datetime
import numpy as np
from typing import (
    List,
    Any,
    Dict
)

from openfinance.config import Config
from openfinance.strategy.feature.base import Feature
from openfinance.strategy.operator.base import OperatorManager

class WinCostDist(Feature):
    name = "WinCostDist"    
    def eval(
        self,
        *args,
        **kwargs
    ):
        """
            Function to evaluate specific stocks
        """
        result = 0
        name = kwargs.get("name")
        data = kwargs.get("data", None)
        # print("data: ", data, "name: ", name)
        chip = {}
        def calc_by_mean(
            high,
            low,
            vol,
            turnover,
            div,
            A
        ):
            minD = (high - low)/div
            x = [round(low + i * minD, 2) for i in range(div)]
            #print(x)
            minVol = vol/div
            for k,v in chip.items():
                chip[k] = chip[k] * (1 - turnover/100 * A)
            for i in x:
                if i in chip:
                    chip[i] += minVol * turnover/100 * A
                else:
                    chip[i] = minVol * turnover/100 * A

        def win_rate(
            price
        ):
            total = 0.000001
            win = 0
            for k, v in chip.items():
                total += v
                if k < price:
                    win += v
            return win/total

        if len(data):
            last_price = data[len(data)-1][2]
            for d in data:
                try:
                    calc_by_mean(d[0],d[1],d[3],d[4], 10, 1)
                except:
                    if not d[4]:
                        calc_by_mean(d[0],d[1],d[3],0.0, 10, 1)
                    print("d:", d)
                    continue
            result = win_rate(last_price)
        #print(chip)
        return result