# views1.py  
from fastapi import APIRouter, Body

router = APIRouter(  
    prefix="/api/v1",  # 前缀，所有路由都会加上这个前缀  
    tags=["icon"]    # 标签，用于API文档分类  
)  

@router.get("/credentials")  
async def get_all_credentials():
    return {}

@router.get("/components-credentials")  
async def get_all_com_credentials():
    return {}

@router.post("/credentials")
async def create_credentials(data: dict = Body(...)):
    return {}

@router.get("/credentials/{credentialName}")  
async def get_credential_by_name(credentialName: str):
    return ""

@router.get("/components-credentials/{name}")  
async def get_com_credential_by_name(name: str):
    return {}

@router.get("/credentials/{id}")  
async def get_credential_by_id(id: str):
    return ""

@router.post("/node-load-method/{name}")  
async def get_node_cred_by_name(name: str, data: dict = Body(...)):
    return []