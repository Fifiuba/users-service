from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .controllers import user_controller
from .database.database import engine
from .database import models

origins = [

    # Cambiar por api-gateway
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app = FastAPI()
app.include_router(user_controller.user_router, prefix="/users", tags=["Users"])


@app.get("/")
async def root():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
