import uvicorn
from users_service.app import app
from users_service.utils import firebase_handler
from users_service.database import database
from users_service.utils import events_handler
from users_service.utils import wallet_handler

########

events_handler.init_events()
database.init_database()
firebase_handler.init_firebase()
wallet_handler.init_wallet()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
