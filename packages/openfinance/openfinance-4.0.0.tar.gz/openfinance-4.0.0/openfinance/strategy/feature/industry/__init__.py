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

FeatureManager().register([
    PositiveNewsSentiment,
    NegativeNewsSentiment
])


FeatureManager().register_from_file(
    "openfinance/strategy/feature/industry/feature_id.json"
)