import uvicorn
from users_service.app import app
from users_service.utils import firebase_handler
from users_service.database import database


database.init_database()
firebase_handler.init_firebase()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
