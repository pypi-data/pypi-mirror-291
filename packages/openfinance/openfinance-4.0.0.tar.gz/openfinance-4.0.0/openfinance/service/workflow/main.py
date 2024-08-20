from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware  

from openfinance.utils.log import get_logger
from openfinance.service.workflow.routers import (
    flows, 
    tools, 
    skills, 
    agents, 
    marketplace, 
    icons, 
    nodes,
    llmfactors,
    quantfactors
)

app = FastAPI()

origins = [  
    # "http://localhost:3000",  # 假设你的React应用运行在3000端口  
    "*"  # 允许所有源，但出于安全考虑，最好明确指定允许的源  
]

app.add_middleware(  
    CORSMiddleware,  
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
) 

@app.get("/") 
async def connect():  
    return {"Hello": "World"}

app.include_router(flows.router)  
app.include_router(tools.router)
app.include_router(skills.router)  
app.include_router(agents.router)
app.include_router(marketplace.router)
app.include_router(icons.router)
app.include_router(nodes.router)
app.include_router(llmfactors.router)
app.include_router(quantfactors.router)

if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=5009)