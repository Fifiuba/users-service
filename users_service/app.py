from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers import user_controller
from .database.crud import logger


# Post events

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.events_api import EventsApi
from datadog_api_client.v1.model.event_create_request import EventCreateRequest

body = EventCreateRequest(
    title="Starting server",
    text="User service starting",
    priority="low",
    alert_type="info",
    host="users-service",
    tags=[
        "test:Example",
    ],
)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = EventsApi(api_client)
    response = api_instance.create_event(body=body)

    print(response)

logger.info("Starting server")

########

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_controller.user_router, prefix="/users", tags=["Users"])
