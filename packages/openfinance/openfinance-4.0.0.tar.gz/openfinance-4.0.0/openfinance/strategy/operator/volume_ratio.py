import numpy as np
import pandas as pd
from openfinance.strategy.operator.base import Operator

try:
    import talib
    
    class VolumeRatio(Operator):
        name:str = "VolumeRatio"

        def run(
            self,
            data,
            **kwargs
        ):
            """
            Calculate the Volume Ratio Indicator.
            
            Parameters:
            data (pd.DataFrame): A DataFrame containing 'Close' and 'Volume' columns.
            
            Returns:
            pd.Series: The Volume Ratio Indicator series.
            """
            data = pd.DataFrame({
                "Close": data[0],
                "Volume": data[1]
            })
            # Calculate the daily price change
            data['Change'] = data['Close'].diff()
            
            # Initialize columns for up volume and down volume
            data['Up_Volume'] = 0
            data['Down_Volume'] = 0
            
            # Assign volume to up or down volume based on price change
            data.loc[data['Change'] > 0, 'Up_Volume'] = data['Volume']
            data.loc[data['Change'] < 0, 'Down_Volume'] = data['Volume']
            
            # Calculate the cumulative up volume and down volume
            data['Cum_Up_Volume'] = data['Up_Volume'].cumsum()
            data['Cum_Down_Volume'] = data['Down_Volume'].cumsum()
            
            # Calculate the Volume Ratio Indicator
            data['Volume_Ratio'] = data['Cum_Up_Volume'] / data['Cum_Down_Volume']
            
            # Fill NaN values with 1 (for the first row where there is no previous data)
            data['Volume_Ratio'].fillna(1, inplace=True)
            
            result = data['Volume_Ratio']

            if latest:
                return result[-1]
            
            return result.tolist()

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