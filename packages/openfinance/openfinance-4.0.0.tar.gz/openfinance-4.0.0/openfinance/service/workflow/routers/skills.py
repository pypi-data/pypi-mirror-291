# views1.py  
from fastapi import APIRouter  
from openfinance.config import Config
from openfinance.agents.workflow.node_manager import NodeManager

manger = NodeManager()

router = APIRouter(  
    prefix="/api/v1/skills",  # 前缀，所有路由都会加上这个前缀  
    tags=["skill"]    # 标签，用于API文档分类  
)  

@router.get("/")  
async def get_all_skills():
    result = []
    index = 0 
    for k, v in manger.nodes.items():
        if "Skill" in v.params["baseClasses"]:
            schemas = [
                {"property": item, "type": "string", "description": item, "required": True} for item in v.node.inputs
            ]                 
            role_schema = v.node.schema()
            if role_schema:
                schemas += role_schema
            params = {
                "id": index,
                "name": k,
                "color": "linear-gradient(rgb(178,218,248), rgb(76,242,57))",
                "description": v.node.description,
                "schema": schemas,
                "iconSrc": "",
                "func": "test_prompt",
                "createdDate": "2024-05-29T02:03:40.000Z",
                "updatedDate": "2024-05-29T02:03:40.000Z"
            }
            index += 1
            result.append(params)
    return result