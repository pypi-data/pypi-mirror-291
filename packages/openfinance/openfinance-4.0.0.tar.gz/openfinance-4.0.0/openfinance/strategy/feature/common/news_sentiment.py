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


NO_DIVIDENT = -100000

class PositiveNewsSentiment(Feature):
    name = "PositiveNewsSentiment"
    def eval(
        self,
        *args,
        **kwargs
    ):
        """
            Function to evaluate specific stocks
        """
        # result = 0
        result = []
        data = kwargs.get("data")
        if len(data):
            # print(data)
            data = data[0]
            days = data.split(",")
            for d in days:
                s = d.split(":")
                #result += int(s[0])
                result.append(float(s[0]))
        return OperatorManager().get("MovingAverage").run(result)

class NegativeNewsSentiment(Feature):
    name = "NegativeNewsSentiment"
    def eval(
        self,
        *args,
        **kwargs
    ):
        """
            Function to evaluate specific stocks
        """
        # result = 0
        result = []
        data = kwargs.get("data")
        if len(data):
            # print(data)
            data = data[0]
            days = data.split(",")
            for d in days:
                s = d.split(":")
                #result += int(s[0])
                result.append(float(s[2]))
        return OperatorManager().get("MovingAverage").run(result)