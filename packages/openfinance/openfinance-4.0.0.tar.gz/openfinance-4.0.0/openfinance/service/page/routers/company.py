# views1.py  
import traceback
from fastapi import APIRouter, Body

from openfinance.config import Config
from openfinance.config import HOMELOG

from openfinance.service.error import StatusCodeEnum, wrapper_return
from openfinance.datacenter.knowledge.entity_graph.base import EntityGraph

from openfinance.service.page.manager  import PageManager
from openfinance.agents.plugin.memory.user import UserManager
from openfinance.strategy.profile.base import ProfileManager

router = APIRouter(  
    prefix="/api/v1/company",  # 前缀，所有路由都会加上这个前缀  
    tags=["company"]    # 标签，用于API文档分类  
)

manager = PageManager()
profile_manager = ProfileManager()

EG = EntityGraph()

@router.post("/data")
async def eval(data: dict = Body(...)):   
    try:
        print("data: ", data)
        code = data.get("code", "600519")
        name = data.get("name", "贵州茅台")
        data = await manager.get("company").fetch(code=code, name=name)
        return data
    except Exception as e:
        print(e)
        traceback.print_exc()  
        traceback_str = traceback.format_exc()  
        print("堆栈跟踪字符串:\n", traceback_str)
        return

@router.post("/tags")
async def eval(data: dict = Body(...)):   
    try:
        print("data: ", data)
        company = data.get("company", "贵州茅台")
        data = profile_manager.fetch_by_company(company)
        return data
    except Exception as e:
        print(e)
        traceback.print_exc()  
        traceback_str = traceback.format_exc()  
        print("堆栈跟踪字符串:\n", traceback_str)
        return

@router.post("/search")
async def search(data: dict = Body(...)):
    try:
        text = data["data"]['query']
        #print(text)
        companies = EG.search(text)
        data = {
            "result": [{"company": k} for k in companies]
        }
        return wrapper_return(output=data,status=StatusCodeEnum.OK)
    except Exception as e:
        return wrapper_return(status=StatusCodeEnum.UNKNOWN_ERROR)