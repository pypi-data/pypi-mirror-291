import time
import json
from fastapi import APIRouter, Body
from openfinance.agents.workflow.manager import WorkflowManager

manager = WorkflowManager()

router = APIRouter(  
    prefix="/api/v1/chatflows",  # 前缀，所有路由都会加上这个前缀  
    tags=["workflow"]    # 标签，用于API文档分类  
)

@router.get("/")  
async def get_all_flows():
    result = []
    for k, v in manager.flows.items():
        jsondata = json.load(open(v.filename, "r"))
        if "flowData" in jsondata: 
            result.append(jsondata) # user defined format
        else:
            params = {
                "id": jsondata.get("id", 0),
                "name": k,
                "flowData": json.dumps(jsondata),
                "badge": jsondata.get("badge", ""),
                "framework": jsondata.get("framework", ""),
                "categories": jsondata.get("categories", ""),
                "type": "Chatflow",
                "description": jsondata.get("description", "")
            }
            result.append(params)
    return result

@router.get("/{id}") 
async def get_flow_by_id(id: int):
    flow = manager.get_flow_by_id(id)
    jsondata = json.load(open(flow.filename, "r"))
    if "flowData" in jsondata: 
        return jsondata
    result = {
        "name": jsondata.get("name", ""),
        "flowData": json.dumps(jsondata),
        "badge": jsondata.get("badge", ""),
        "framework": jsondata.get("framework", ""),
        "categories": jsondata.get("categories", ""),
        "type": "Chatflow",
        "description": jsondata.get("description", "")
    }
    return result


@router.put("/{id}") 
async def get_flow_by_id(id: int, data: dict = Body(...)):
    flow = manager.get_flow_by_id(id)   
    flow.update_graph(data)
    return data

@router.post("/")  
async def save_flow(data: dict = Body(...)):
    name = data["name"]
    data["id"] = str(time.time_ns())
    data.update({
        "type": "CHATFLOW",
        "apikeyid": None,
        "chatbotConfig": None,
        "apiConfig": None,
        "analytic": None,
        "speechToText": None,
        "category": None,
        "createdDate": time.ctime(),
        "updatedDate": time.ctime()
    })
    filename = f"openfinance/agents/third_party/workflow/{name}.json"
    with open(filename, "w") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)
    manager.add(filename)
    return data