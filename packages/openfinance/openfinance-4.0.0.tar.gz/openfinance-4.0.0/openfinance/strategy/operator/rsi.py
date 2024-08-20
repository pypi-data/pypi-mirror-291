import numpy as np

from openfinance.strategy.operator.base import Operator

try:
    import talib

    class RSI(Operator):
        name:str = "RSI"

        def run(
            self,
            data,
            **kwargs
        ):
            """
                获取RSI指标
            """
            latest = kwargs.get("latest", True)
            rsi = talib.RSI(np.array(data, dtype='double'))
            if latest:
                return rsi[-1]
            return rsi.tolist() 

except Exception as e:
    
    from openfinance.datacenter.database.quant.quant_engine import Engine

    class RSI(Operator):
        name:str = "RSI"

        def run(
            self,
            data,
            **kwargs
        ):
            """
                Function to evaluate specific stocks
            """
            latest = kwargs.get("latest", True)

            rsi = Engine.process(
                factor=self.name,
                quant_data=data,
                ext=kwargs          
            )

            if latest and isinstance(rsi, list):
                return rsi[-1]
            return rsi



