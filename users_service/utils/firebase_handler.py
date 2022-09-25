import os

if "RUN_ENV" in os.environ.keys() and os.environ["RUN_ENV"] == "test":

    from users_service.utils.firebase_mock import FirebaseMock

    firebase = FirebaseMock()
    default_app = "def"


else:
    from users_service.utils.firebase_implementation import Firebase
    import firebase_admin
    from firebase_admin import credentials, auth

    cred = credentials.Certificate("users_service/utils/firebase_keys.json")

    default_app = firebase_admin.initialize_app(cred)

    firebase = Firebase(auth, default_app)


def get_fb():
    try:
        yield firebase
    finally:
        firebase
