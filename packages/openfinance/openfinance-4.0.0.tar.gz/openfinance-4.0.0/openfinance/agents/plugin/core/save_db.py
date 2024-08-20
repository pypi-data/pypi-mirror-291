import asyncio

from typing import (
    Any,
    Callable,
    Dict,
    Union,
    List
)
from openfinance.agentflow.base import Runnable
from openfinance.config.config import Config
from openfinance.utils.time import get_current_date
from openfinance.datacenter.database.base import DataBaseManager

DBM = DataBaseManager(Config())

class SaveDB(Runnable):
    """
        Base Runnable
    """
    name: str = "savedb"
    output: str = "output"
    inputs: List[str] = ["content"]
    input_params: List[str] = ["db", "table", "columns"]
    description: str = "A runnable plugin to storage info to db"

    async def acall(
        self,
        **kwargs: Any        
    ) -> Any:
        db_name = kwargs.get("db")
        db_table = kwargs.get("table")
        columns = kwargs.get("columns").split("|")
        db_data = {}
        # if inputs is dict format, spread them
        for o in self.inputs:
            if o in kwargs and isinstance(kwargs[o], dict):
                tempk = kwargs.pop(o)
                kwargs.update(tempk)

        for col in columns:
            if col == "TIME" or col == "DATE":
                db_data[col] = get_current_date()
            else:
                db_data[col] = kwargs.get(col, "")
        result = DBM.get(db_name).insert(
            db_table,
            db_data,
            dup_key=columns
        )
        return {self.output: kwargs}