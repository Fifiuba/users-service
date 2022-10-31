from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers import user_controller

import json_log_formatter
import logging
from ddtrace import patch; patch(logging=True)

import uvicorn
from users_service.utils import firebase_handler
from users_service.database import database


database.init_database()
firebase_handler.init_firebase()

formatter = json_log_formatter.JSONFormatter()

json_handler = logging.FileHandler(filename='./logs.log')
json_handler.setFormatter(formatter)

logger = logging.getLogger('users_service_logger')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

def starting_log():
    logger.info('Starting server', extra={'referral_code': '52d6ce'})

starting_log()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_controller.user_router, prefix="/users", tags=["Users"])
