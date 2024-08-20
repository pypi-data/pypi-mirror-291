# views1.py  
from fastapi import APIRouter
from starlette.responses import FileResponse 
# from openfinance.agents.workflow.manager import WorkflowManager

# manager = WorkflowManager()

router = APIRouter(  
    prefix="/api/v1/node-icon",  # 前缀，所有路由都会加上这个前缀  
    tags=["icon"]    # 标签，用于API文档分类  
)  
  
@router.get("/{name}")  
async def get_icon_by_name(name: str):
    result = []
    index = 0
    iconpath = "openfinance/agents/third_party/node/base.svg"
    return FileResponse(iconpath)