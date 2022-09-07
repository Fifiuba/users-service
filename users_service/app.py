import uvicorn
from fastapi import FastAPI
from .controllers import user_controller

app = FastAPI()

app.include_router(user_controller.user_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

    
