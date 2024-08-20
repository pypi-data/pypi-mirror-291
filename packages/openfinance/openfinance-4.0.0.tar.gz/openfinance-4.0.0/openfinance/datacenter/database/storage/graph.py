import pandas
import time
from openfinance.config import Config
from sqlalchemy.types import VARCHAR
from openfinance.datacenter.database.base import DataBaseManager

from openfinance.datacenter.knowledge.entity_graph.build_graph import GraphBuilder

config = Config()

def store_graph( 
    init=False
):
    if init:
        rb = GraphBuilder(reload=init)
        rb.init_data()