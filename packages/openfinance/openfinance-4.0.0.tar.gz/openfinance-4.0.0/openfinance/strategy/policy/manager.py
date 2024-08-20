import os
import asyncio
import aiohttp
import json

from abc import ABC, abstractmethod

from typing import (
    Any,
    List,
    Dict,
    Union
)

from openfinance.strategy.policy.base import Strategy
from openfinance.strategy.policy.lr_ranker import LRPolicy
from openfinance.strategy.policy.index_ranker import IndexPolicy
from openfinance.utils.singleton import singleton

@singleton
class StrategyManager:
    name_to_strategies: Dict[str, Strategy] = {}
    def __init__(
        self
    ):
        company_file = "openfinance/strategy/policy/config/company/"
        for filename in os.listdir(company_file):
            filepath = company_file + filename
            lr_instance = LRPolicy.from_file(filename=filepath)
            index_instance = IndexPolicy.from_file(filename=filepath)
            self.update(lr_instance)
            self.update(index_instance)

        market_file = "openfinance/strategy/policy/config/market/"
        for filename in os.listdir(market_file):
            filepath = market_file + filename
            lr_instance = LRPolicy.from_file(filename=filepath)
            self.update(lr_instance)

    @property
    def strategy(
        self
    ):
        return self.name_to_strategies

    def update(
        self,
        instance: Union[Strategy, Dict[str, Strategy]]
    ):
        if isinstance(instance, dict):
            self.name_to_strategies.update(instance)
        else:
            self.name_to_strategies[instance.name + "-" + instance.model.name] = instance
    
    def get(
        self,
        name: str = "general",
        model: str = "LRSort"        
    ):
        key = name + "-" + model
        return self.name_to_strategies.get(key, None)

    def add(
        self,
        filename: str
    ):
        # lr at this moment
        lr_instance = LRPolicy.from_file(filename=filename)
        self.update(lr_instance)