# views1.py  
import traceback
from fastapi import APIRouter, Body

from openfinance.config import Config
from openfinance.config import HOMELOG

from openfinance.service.error import StatusCodeEnum, wrapper_return
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph

from openfinance.service.page.manager  import PageManager
from openfinance.agents.plugin.memory.user import UserManager


router = APIRouter(  
    prefix="/api/v1/macro",  # 前缀，所有路由都会加上这个前缀  
    tags=["macro"]    # 标签，用于API文档分类  
)

manager = PageManager()
EG = EntityGraph()

@router.post("/data")
async def eval(data: dict = Body(...)):   
    try:
        # print("data: ", data)
        company = data.get("country", "CHINA")
        data = await manager.get("macro").fetch(name=company)
        return data
    except Exception as e:
        print(e)
        traceback.print_exc()  
        traceback_str = traceback.format_exc()  
        print("堆栈跟踪字符串:\n", traceback_str)
        return