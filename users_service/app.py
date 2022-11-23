from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers import user_controller
from .database.crud import logger
from fastapi import status

logger.info("Starting server")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root(status_code=status.HTTP_200_OK):
    message = {"service": "Users Service!", "created_on": "7-9-22", "description": "User services is the responsable of handle the users of the fifiuba app"}
    return message
app.include_router(user_controller.user_router, prefix="/users", tags=["Users"])
