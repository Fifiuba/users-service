from datadog_api_client.v1.model.event_create_request import EventCreateRequest
from datadog_api_client.v1.api.events_api import EventsApi


class EventsGenerator:
    def __init__(self, configuration, api_client):
        self.configuration = configuration
        self.api_client = api_client

    def create_event(self, titleEvent, textEvent, alert_typeEvent, tagsEvent):
        body = EventCreateRequest(
            title=titleEvent,
            text=textEvent,
            priority="normal",
            alert_type=alert_typeEvent,
            host="users-service",
            tags=tagsEvent,
        )
        api_instance = EventsApi(self.api_client)
        api_instance.create_event(body=body)
