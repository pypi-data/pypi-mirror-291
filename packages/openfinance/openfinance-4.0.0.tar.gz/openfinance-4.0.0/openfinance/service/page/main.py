from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware  

from openfinance.service.page.routers import (
    company, market, chathome, macro
)

app = FastAPI()

origins = [
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

app.include_router(company.router)  
app.include_router(market.router)
app.include_router(chathome.router)
app.include_router(macro.router)

if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=5002)