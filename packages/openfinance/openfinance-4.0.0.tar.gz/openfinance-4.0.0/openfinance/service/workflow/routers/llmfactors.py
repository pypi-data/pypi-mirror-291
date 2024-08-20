import json
import inspect
from fastapi import APIRouter  
from openfinance.datacenter.knowledge.executor import ExecutorManager

router = APIRouter(  
    prefix="/api/v1/llmfactors",  # 前缀，所有路由都会加上这个前缀  
    tags=["llmfactors"]    # 标签，用于API文档分类  
)  

manager = ExecutorManager()

@router.get("/")  
async def get_all_tools():
    result = []
    index = 0
    
    for k, exe in manager.executors.items():
        if k in manager.config:
            func = json.dumps(manager.config[k], indent=4)
        else:
            func = inspect.getsource(exe.func)
        
        desc = exe.description
        if "zh" in exe.extend:
            desc += "(" + str(exe.extend["zh"])+ ")"
        params = {
            "id": index,
            "name": k,
            "color": "linear-gradient(rgb(178,218,248), rgb(76,242,57))",
            "description": desc,
            "schema": [],
            "iconSrc": "",
            "func": func,
            "createdDate": "2024-05-29T02:03:40.000Z",
            "updatedDate": "2024-05-29T02:03:40.000Z"
        }
        index += 1
        result.append(params)
    return result