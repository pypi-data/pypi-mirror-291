import requests
import numpy as np
import json

from openfinance.config.macro import MLOG
token = '8140ad230f687daede75a08855e8ae5ff40c3ba8'
url = 'http://114.132.71.128:5001/'

class Engine:
    @staticmethod
    def process(
        factor=None,
        quant_data=None,
        ext = {}
    ):
        json_map = {
            'factor': factor,
            'quant_data': quant_data,
            'ext': ext,
            'token': token
        }
        # print(json_map)
        MLOG.debug(f"json_map: {json_map}")
        r = requests.post(url + 'quant/calc', json=json_map)
        try:
            if r.status_code == 200:
                jsondata = json.loads(r.text)
                if jsondata['status'] == 0:
                    data = jsondata['result']
                    # print(data)
                    MLOG.debug(f"data: {data}")
                    if isinstance(data, list):
                        return [0 if np.isnan(x) else round(x, 2) for x in data]
                    elif isinstance(data, dict):
                        result = {}
                        for k, v in data.items():
                            if isinstance(v, list):
                                result[k] = [0 if np.isnan(x) else round(x, 2) for x in v]
                            else:
                                result[k] = v
                        return result
                    else:
                        return data
                else:
                    MLOG.info(f"jsondata: {jsondata}")
            else:
                 MLOG.info(f"r: {r}")
        except Exception as e:
            MLOG.error(f"e: {e}")
