import json 
from fastapi import APIRouter  
from openfinance.agents.agent.manager import RoleManager
from openfinance.agentflow.llm.manager import ModelManager
from openfinance.config import Config

llm = ModelManager(Config()).get_model("aliyungpt")

manager = RoleManager()

router = APIRouter(  
    prefix="/api/v1/agents",  # 前缀，所有路由都会加上这个前缀  
    tags=["agent"]    # 标签，用于API文档分类  
)  

@router.get("/")  
async def get_all_agents():
    result = []
    idx = 1
    for k, v in manager.roles.items():
        params = {
            "id": idx,
            "name": k,
            "description": v["kwargs"]["description"],
            "schema": manager.plugins(k),
            "func": manager.prompt(k),
            "iconSrc": "",
            "createdDate": "2024-05-29T02:03:40.000Z",
            "updatedDate": "2024-05-29T02:03:40.000Z"            
        }           
        result.append(params)
    return result

@router.get("/id")  
async def get_agent_by_id(id: int):
    agent = manager.get_role_by_id(id)
    name = agent["name"]
    result = {
        "id": id,
        "name": name,
        "color": "linear-gradient(rgb(178,218,248), rgb(76,242,57))",
        "description": agent["kwargs"]["description"],
        "schema": manager.plugins(name),
        "iconSrc": "",
        "func": manager.prompt(name),
        "createdDate": "2024-05-29T02:03:40.000Z",
        "updatedDate": "2024-05-29T02:03:40.000Z"
    }
    return result