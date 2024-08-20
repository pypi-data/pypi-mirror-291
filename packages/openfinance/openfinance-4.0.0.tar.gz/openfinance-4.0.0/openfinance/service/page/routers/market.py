# views1.py  
from fastapi import APIRouter, Body
from openfinance.config import Config

from openfinance.strategy.operator.base import OperatorManager
from openfinance.service.error import StatusCodeEnum, wrapper_return
from openfinance.datacenter.database.base import DataBaseManager
from openfinance.strategy.feature.base import FeatureManager
from openfinance.strategy.policy.manager import StrategyManager
from openfinance.strategy.llm_generator.llm_manager import StrategyLLMManager

from openfinance.datacenter.database.source.event.jin10 import (
    get_economic,
    get_event
)

router = APIRouter(  
    prefix="/api/v1/market",  # 前缀，所有路由都会加上这个前缀  
    tags=["market"]    # 标签，用于API文档分类  
)  

NAME = "上证指数"

DBMG = DataBaseManager(Config())
manager = StrategyManager()
llmmanager = StrategyLLMManager()
market_danger = manager.get(name="Volatility")
market_sentiment = manager.get(name="Sentiment")
company_ranker = manager.get(model="IndexPolicy")

@router.get("/sentiment")  
async def get_sentiment():
    try:
        senti = market_sentiment.run(
            candidates = [NAME],
            from_db=True,
            type="market",
            latest=True     
        )
        # print("senti: ", senti)
        senti["text"] = llmmanager.get_llm_content(
            entity_type='Market', 
            role='Sentiment'
        )

        features = market_sentiment.features(
            candidates=[NAME],
            from_db=True,
            type="market"
        )
        result = {}
        for k, v in features.items():
            v["text"] = llmmanager.get_llm_content(
                entity_type='Market', 
                role=k
            )
            result[market_sentiment.name_to_features[k].desc] = v

        result = {
            "summary": senti,
            "features": result
        }
        return wrapper_return(result=result,status=StatusCodeEnum.OK)
    except Exception as e:
        return wrapper_return(status=StatusCodeEnum.UNKNOWN_ERROR)

@router.get("/danger")  
async def get_danger():
    try:
        senti = market_danger.run(
            candidates = [NAME],
            from_db=True,
            type="market",
            latest=True     
        )
        # print("senti: ", senti)        
        senti["text"] = llmmanager.get_llm_content(
            entity_type='Market', 
            role='Volatility'
        )
        features = market_danger.features(
            candidates=[NAME],
            from_db=True,        
            type="market"
        )
        # print("features: ", features)        
        result = {}
        for k, v in features.items():
            v["text"] = llmmanager.get_llm_content(
                entity_type='Market', 
                role=k
            )
            result[market_danger.name_to_features[k].desc] = v

        result = {
            "summary": senti,           
            "features": result
        }
        return wrapper_return(result=result,status=StatusCodeEnum.OK)
    except Exception as e:
        return wrapper_return(status=StatusCodeEnum.UNKNOWN_ERROR)

@router.get("/stock")  
async def get_stock():
    try:
        stocks = company_ranker.run(
            from_db=True,
            type="company"
        )

        features = company_ranker.features(
            candidates= list(stocks.keys()),
            from_db=True,
            type="company"
        )

        result = {
            company_ranker.name_to_features[k].desc: v for k, v in features.items()
        }

        result = {
            "summary": stocks,
            "features": result
        }
        return wrapper_return(result=result,status=StatusCodeEnum.OK)
    except Exception as e:
        return wrapper_return(status=StatusCodeEnum.UNKNOWN_ERROR)


@router.post("/event")
async def event(data: dict = Body(...)):
    try:
        # print("data: ", data)
        DATE = data["data"].get('date', "")
        data = {
            "economic": get_economic(DATE),
            "event": get_event(DATE),
            "future_economic": {},
            "future_event": {}
        }
        # print("data: ", data)
        return wrapper_return(data=data,status=StatusCodeEnum.OK)
    except Exception as e:
        return wrapper_return(status=StatusCodeEnum.UNKNOWN_ERROR)

@router.post("/brief_event")
async def event(data: dict = Body(...)):
    try:
        # print("data: ", data)
        DATE = data["data"].get('month', "2024-08")
        data = await DBMG.get("async_db").exec(
            f"select DATE, data, type from t_daily_event where DATE like '{DATE}%'"
        )
        # print("data: ", data)
        return wrapper_return(data=data,status=StatusCodeEnum.OK)
    except Exception as e:
        return wrapper_return(status=StatusCodeEnum.UNKNOWN_ERROR)