import asyncio
import aiohttp
import json

from abc import ABC, abstractmethod

from typing import (
    Any,
    List,
    Dict
)

from openfinance.strategy.policy.base import Strategy
from openfinance.strategy.model.linear_regression import LR
from openfinance.strategy.feature.base import FeatureManager


class LRPolicy(Strategy):
    @classmethod
    def from_file(
        cls,
        filename="openfinance/strategy/policy/config/company/general.json",
        **kwargs
    ) -> "LRPolicy":
        weights = json.load(open(filename, "r"))
        kwargs.update(weights)
        name = kwargs.get("name")
        desc = kwargs.get("desc", name)

        conf_json = json.load(
            open("openfinance/strategy/policy/config/feature_conf.json", "r")
        )
        feat_to_conf = {}
        for k, c in conf_json.items():
            feat_to_conf.update(c)

        confs = {}
        for feat, val in weights["weights"].items():
            if feat in feat_to_conf:
                for conf_name, conf_val in feat_to_conf[feat].items():
                    if conf_name in confs:
                        confs[conf_name][feat] = conf_val
                    else:
                        confs[conf_name] = {feat: conf_val}
        kwargs.update(confs)
        print("confs: ", confs)

        model = LR.from_conf(**kwargs)
        name_to_features = {k: FeatureManager().get(k) for k in model.features_to_weights.keys()}
        return cls(
            name = name,
            desc = desc,
            model = model,
            name_to_features = name_to_features
        )

    def run(
        self,
        *args,
        **kwargs
    ):  
        print("LRPolicy kwargs: ", kwargs)
        result = super().run(*args, **kwargs)
        print(result)
        if self.name == "Sentiment":
            return {k: 100 * v / (v + 93273089939) for k, v in result.items()}
        elif self.name == "Volatility":
            return {k: 100 * v / (v + 100) for k, v in result.items()}
        return result

if __name__== "__main__":
    
    # pl = LRPolicy.from_file(
    #     filename="openfinance/strategy/policy/config/market.json", 
    #     role="Sentiment"
    # )
    # result = pl.run(
    #     candidates = ["上证指数"],        
    #     from_db=True,
    #     type="market",
    #     latest=True                
    # )
    # print(result)

    pl = LRPolicy.from_file()
    # candidates = pl.fetch(
    #     params=[
    #         # ("OperationGrow", "gt", 10), 
    #         # ("DividentMean", "gt", 3),
    #         # ("DividentSpeed", "gt", 0.1),            
    #         # ("OperationSpeedAcc", "lt", 10),
    #         # ("ProfitGrow", "gt", 10),
    #         # ("ProfitSpeedAcc", "lt", 10),
    #         # ("GrossProfit", "gt", 100),
    #         ("PriceEarning", "lt", 80),
    #         ("PriceEarning", "gt", 10) 
    #         # ("MoneyFlowDirect", "gt", 0)
    #     ])  
    # print(candidates)

    # result = pl.run(
    #     candidates = list(candidates),        
    #     from_db=True,
    #     type="company" 
    # )
    # print(result)

    result = pl.run( 
        from_db=True,
        type="company" 
    )
    print(result)