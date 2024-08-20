import numpy as np
from openfinance.config.macro import MLOG
from openfinance.strategy.operator.base import Operator

try:
    from talib.abstract import *

    class MAConDiv(Operator):
        name:str = "MACD"

        def run(
            self,
            data,
            **kwargs
        ):
            """
                获取MACD指标
            """
            fastperiod = kwargs.get("fastperiod", 12)
            slowperiod = kwargs.get("slowperiod", 26)
            signalperiod = kwargs.get("signalperiod", 9)
            latest = kwargs.get("latest", True)
            intermidate = kwargs.get("intermidate", False)
            if isinstance(data, list):
                macd, macdsignal, macdhist = MACD(
                    np.array(data, dtype='double'), 
                    fastperiod, 
                    slowperiod, 
                    signalperiod
                )
            if intermidate:
                if latest:
                    return {
                        "macd": macd[-1], 
                        "signal" : macdsignal[-1],
                        "hist": macdhist[-1]
                    }
                else:
                    return {
                        "macd": macd, 
                        "signal" : macdsignal,
                        "hist": macdhist
                    }
            else:
                if latest:
                    return macdhist[-1]
                return macdhist.tolist()
              
except Exception as e:

    from openfinance.datacenter.database.quant.quant_engine import Engine

    class MAConDiv(Operator):
        name:str = "MACD"

        def run(
            self,
            data,
            **kwargs
        ):
            """
                Function to evaluate specific stocks
            """
            MLOG.debug(f"data: {data}")    
            if isinstance(data, list):             
                result = Engine.process(
                    factor=self.name,
                    quant_data=data,
                    ext=kwargs
                )
                return result               