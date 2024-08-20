from fastapi import APIRouter
from starlette.responses import FileResponse 
from openfinance.agents.workflow.node_manager import NodeManager

manger = NodeManager()

router = APIRouter(  
    prefix="/api/v1/nodes",  # 前缀，所有路由都会加上这个前缀  
    tags=["icon"]    # 标签，用于API文档分类  
)  

@router.get("/")  
async def get_nodes():
    result = []
    for k, v in manger.nodes.items():
        params = {
            "id": v.id,
            "tags": ["Openfinance"],
            "framework": "Openfinance"
        }
        params.update(v.params)
        params["inputParams"] = v.inputParams
        params["inputAnchors"] = v.inputAnchors
        params["outputAnchors"] = v.outputAnchors
        params["inputs"] = v.inputs
        params["outputs"] = v.outputs                
        result.append(params)
    return result

@router.get("/{name}")  
async def get_nodes_by_name(name: str):
    pass