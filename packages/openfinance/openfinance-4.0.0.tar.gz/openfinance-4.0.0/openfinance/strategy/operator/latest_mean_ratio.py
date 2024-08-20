import numpy as np
import traceback
from openfinance.strategy.operator.base import Operator


NO_DIVIDENT = -100000

class Latest2MeanRatio(Operator):
    name:str = "Latest2MeanRatio"

    def run(
        self,
        data,
        **kwargs
    ):
        """
            获取最新的指标和最近window范围内的比值
        """
        try:
            # print("data: ", data)
            latest = kwargs.get("latest", True)            
            result = []
            if isinstance(data, list): # db select format
                window = kwargs.get("window", len(data) - 1)
                assert len(data) > window + 1, f"data is shorter than {window}"
                for i in range(window, len(data)):
                    total = 0
                    for d in data[i-window:i]:
                        total += d
                    val = data[i]
                    if total:
                        result.append(val * window / total)
            if latest and len(result):
                return result[-1]
            return result
        except Exception as e:
            print(e)
            traceback.print_exc()  
            traceback_str = traceback.format_exc()  
            print("堆栈跟踪字符串:\n", traceback_str)  