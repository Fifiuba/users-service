import uvicorn
from users_service.app import app
from users_service.utils import firebase_handler
from users_service.database import database

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

########

database.init_database()
firebase_handler.init_firebase()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
