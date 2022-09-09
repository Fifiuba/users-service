from fastapi import FastAPI
import uvicorn
from .controllers import user_controller
from .database.database import engine
from .database import models

models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)

user_controller.set_engine(engine)

app = FastAPI()
app.include_router(user_controller.user_router)


@app.get("/")
async def root():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
