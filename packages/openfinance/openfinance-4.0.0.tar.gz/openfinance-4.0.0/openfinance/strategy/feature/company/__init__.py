#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Date    ：2024/02/05 20:25 

'''
from openfinance.strategy.feature.base import FeatureManager
from openfinance.strategy.feature.common.news_sentiment import (
    PositiveNewsSentiment,
    NegativeNewsSentiment
)
from openfinance.strategy.feature.company.divident_stability import DividentSpeed
from openfinance.strategy.feature.company.divident_mean import DividentMean
from openfinance.strategy.feature.company.win_cost_distribution import WinCostDist

FeatureManager().register([
    DividentSpeed,
    DividentMean,
    PositiveNewsSentiment,
    NegativeNewsSentiment,
    WinCostDist
])

FeatureManager().register_from_file(
    "openfinance/strategy/feature/company/feature_id.json"
)