import datetime
from typing import (
    Any, Callable, Dict, Optional, Tuple, List, Union
)

from openfinance.config import Config
from openfinance.utils.time import is_workday
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.datacenter.database.storage import stock_func

db = DataBaseManager(Config()).get("init")
db.exec("create database graph")
db.exec("create database financial")
db.exec("create database quantdata")


class DataUpdater:
    '''
        class used for update database
    '''
    func: List[Callable] = []
   
    def load_func(
        self, 
        func: Union[List[Callable], Callable]
    ) -> None:
        if isinstance(func, List):
            self.func += func
        else:
            self.func.append(func)

    def daily_update(
        self,
        init=False
    ) -> None:
        '''
            default function should update latest data
        '''
        is_valid = is_workday(1)
        print("is_valid: ", is_valid)
        if is_valid:
            for func in self.func:
                print(func.__name__)
                try:
                    func(init=init)
                except Exception as e:
                    print(f"daily_update Error for {func.__name__}: ", e)
    
if __name__ == "__main__":
    updater = DataUpdater()
    updater.load_func(
        stock_func
    )
    updater.daily_update(init=False)