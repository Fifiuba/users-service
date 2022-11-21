
def init_events():
    from datadog_api_client import ApiClient, Configuration
    from users_service.utils.events_generator import EventsGenerator
    config = Configuration()
    api_client =  ApiClient(config)
    global events
    events = EventsGenerator(config, api_client)

def get_event():
    print("entre a get event")
    try:
        yield events
    finally:
        events