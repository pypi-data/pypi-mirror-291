#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Date    ：2024/02/05 20:25 

'''


from openfinance.strategy.feature.base import FeatureManager

from openfinance.strategy.feature.market.vix import Vix

FeatureManager().register([
    Vix
])

FeatureManager().register_from_file(
    "openfinance/strategy/feature/market/feature_id.json"
)