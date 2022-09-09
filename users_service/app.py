from fastapi import FastAPI
import uvicorn
from .controllers import user_controller
from .database.database import engine, Base



app = FastAPI()

app.include_router(user_controller.user_router)

user_controller.set_engine(engine)


@app.get("/")
async def root():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
