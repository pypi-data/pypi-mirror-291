import numpy as np

from openfinance.strategy.operator.base import Operator

try:
    import talib
    
    class OnBalanceVolume(Operator):
        name:str = "OBV"

        def run(
            self,
            data,
            **kwargs
        ):
            """
                获取OBV能量指标
            """

            latest = kwargs.get("latest", True)

            close = [a[0] for a in data]
            volume = [a[1] for a in data]
            obv = talib.OBV(
                np.array(close),
                np.array(volume)
            )
            if latest:
                return obv[-1]
            
            return obv.tolist()

except Exception as e:
    
    from openfinance.datacenter.database.quant.quant_engine import Engine
    
    class OnBalanceVolume(Operator):
        name:str = "OBV"

        def run(
            self,
            data,
            **kwargs
        ):
            """
                Function to evaluate specific stocks
            """
            # print(data)
            latest = kwargs.get("latest", True)
            if latest:
                kwargs["latest"] = True
       
            obv = Engine.process(
                factor=self.name,
                quant_data=data,
                ext=kwargs
            )
            if latest and isinstance(obv, list):
                return obv[-1]     
            return obv