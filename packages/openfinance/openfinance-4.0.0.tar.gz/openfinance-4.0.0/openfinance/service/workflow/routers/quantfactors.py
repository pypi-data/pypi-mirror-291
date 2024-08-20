import json
from fastapi import APIRouter  
from openfinance.strategy.feature.base import FeatureManager

manager = FeatureManager()

router = APIRouter(  
    prefix="/api/v1/quantfactors",  # 前缀，所有路由都会加上这个前缀  
    tags=["quantfactors"]    # 标签，用于API文档分类  
)  

@router.get("/")  
async def get_all_factors():
    result = []
    index = 0  
    for k, v in manager.features.items():
        schema = []
        if v.operator:
            schema = [{"property": k, "type": type(v).__name__, "value": v, "required": True} for k, v in v.operator.items()]
        params = {
            "id": index,
            "name": v.desc,
            "color": "linear-gradient(rgb(178,218,248), rgb(76,242,57))",
            "description": v.desc,
            "schema": schema,
            "iconSrc": "",
            "func": json.dumps(v.source, indent=4),
            "createdDate": "2024-05-29T02:03:40.000Z",
            "updatedDate": "2024-05-29T02:03:40.000Z"
        }
        index += 1
        result.append(params)
    return result