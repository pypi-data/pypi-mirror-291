# views1.py  
import traceback
from fastapi import APIRouter, Body

from openfinance.config import Config
from openfinance.config import HOMELOG

from openfinance.service.error import StatusCodeEnum, wrapper_return
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph
from openfinance.agents.plugin.memory.user import UserManager


router = APIRouter(  
    prefix="/api/v1/chat",  # 前缀，所有路由都会加上这个前缀  
    tags=["chat"]    # 标签，用于API文档分类  
)

EG = EntityGraph()
user_manager = UserManager(Config())

@router.post("/sidebar")
async def get_sidebar(data: dict = Body(...)):
    try:
        # print("data: ", data)
        user = data["header"]["user"]        
        data = {
            "stock_list": [{"company": k} for k in EG.search()],
            "role_list": [],
            "history_list": user_manager.get_snapshot(user),
            "task_list": []
        }
        # print("data: ", data)
        return wrapper_return(output=data,status=StatusCodeEnum.OK)
    except Exception as e:
        print(e)
        return wrapper_return(status=StatusCodeEnum.UNKNOWN_ERROR)

@router.post("/history")
async def get_sidebar(data: dict = Body(...)):
    try:
        data = {
            "result": user_manager.get_history(data["data"]["session_id"]),
        }
        return wrapper_return(output=data,status=StatusCodeEnum.OK)
    except Exception as e:
        print(e)
        return wrapper_return(status=StatusCodeEnum.UNKNOWN_ERROR)