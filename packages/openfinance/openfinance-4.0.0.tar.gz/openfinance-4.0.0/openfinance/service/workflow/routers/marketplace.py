import json
from fastapi import APIRouter  
from openfinance.agents.workflow.manager import WorkflowManager

manager = WorkflowManager()

router = APIRouter(  
    prefix="/api/v1/marketplaces",  # 前缀，所有路由都会加上这个前缀  
    tags=["workflow"]    # 标签，用于API文档分类  
)  

@router.get("/templates")  
async def get_all_flows():
    result = []
    index = 0
    for k, v in manager.flows.items():
        index += 1
        jsondata = json.load(open(v.filename, "r"))
        params = {
            "id": index,
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
    result = []
    index = 0
    for k, v in manager.flows.items():
        index += 1
        jsondata = json.load(open(v.filename, "r"))
        params = {
            "id": index,
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

# const getAllTemplates = async () => {
#     try {
#         let marketplaceDir = path.join(__dirname, '..', '..', '..', 'marketplaces', 'chatflows')
#         let jsonsInDir = fs.readdirSync(marketplaceDir).filter((file) => path.extname(file) === '.json')
#         let templates: any[] = []
#         jsonsInDir.forEach((file, index) => {
#             const filePath = path.join(__dirname, '..', '..', '..', 'marketplaces', 'chatflows', file)
#             const fileData = fs.readFileSync(filePath)
#             const fileDataObj = JSON.parse(fileData.toString())
#             const template = {
#                 id: index,
#                 templateName: file.split('.json')[0],
#                 flowData: fileData.toString(),
#                 badge: fileDataObj?.badge,
#                 framework: fileDataObj?.framework,
#                 categories: fileDataObj?.categories,
#                 type: 'Chatflow',
#                 description: fileDataObj?.description || ''
#             }
#             templates.push(template)
#         })




# export default {
#     getAllTemplates
# }
