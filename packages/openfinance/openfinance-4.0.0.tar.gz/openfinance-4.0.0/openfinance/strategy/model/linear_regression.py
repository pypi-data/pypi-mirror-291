import json

from typing import (
    Any,
    List,
    Dict
)

from openfinance.strategy.model.base import Model
from openfinance.strategy.feature.company import *
from openfinance.strategy.feature.market import *
from openfinance.strategy.feature.base import FeatureManager

DEFAULT = -100000

class LR(Model):
    name: str = "LRSort"    
    features_to_weights: Dict[str, float]
    features_to_confs: Dict[str, Any]

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @classmethod
    def from_conf(
        cls,
        **kwargs     
    ) -> "LR":
        return cls(
            features_to_weights = kwargs.get("weights", {}),
            features_to_confs = kwargs.get("confs", {})
        )

    def policy(
        self,
        *args,
        **kwargs    
    ):
        """
            data: dict(feature -> {stock: val})
        """
        name = kwargs.get("name")
        name_to_features = kwargs.get("name_to_features")
        # print(name_to_features)
        result = DEFAULT
        for k, v in name_to_features.items():
            if name in v:
                # print(v, self.features_to_weights)
                result += self.features_to_weights[k] * v[name]
        if result != DEFAULT:
            return result - DEFAULT
        else: 
            return 
