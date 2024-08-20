import numpy as np
from openfinance.config.macro import MLOG
from openfinance.strategy.operator.base import Operator

from talib.abstract import *

class BollingerBand(Operator):
    name:str = "BBand"

    def run(
        self,
        data,
        **kwargs
    ):
        """
            获取MACD指标
        """
        timeperiod = kwargs.get("timeperiod", 5)
        nbdevup = kwargs.get("nbdevup", 2.0)
        nbdevdn = kwargs.get("nbdevdn", 2.0)
        matype = kwargs.get("matype", 0)
        latest = kwargs.get("latest", True)
        intermidate = kwargs.get("intermidate", False)
        if isinstance(data, list):
            upperband, middleband, lowerband = BBANDS(
                np.array(data, dtype='double'), 
                timeperiod=timeperiod, 
                nbdevup=nbdevup, 
                nbdevdn=nbdevdn,
                matype=matype
            )
        if intermidate:
            if latest:
                return {
                    "lowerband": lowerband[-1], 
                    "middleband" : middleband[-1],
                    "upperband": upperband[-1]
                }
            else:
                return {
                    "lowerband": lowerband, 
                    "middleband" : middleband,
                    "upperband": upperband
                }
        else:
            if latest:
                return middleband[-1]
            return middleband.tolist()