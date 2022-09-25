import os

if "RUN_ENV" in os.environ.keys() and os.environ["RUN_ENV"] == "test":

    #from users_service.utils.firebase_mock import FirebaseMock 
    uid= "asdasdasdslwlewed1213123"
    
    def create_user(email, password):
        return uid

    def valid_user(email):
        return uid
        
    def delete_user(uid_user):
        pass

else: 

    from users_service.database import exceptions
    import firebase_admin
    from firebase_admin import credentials, auth
    from firebase_admin import exceptions as fb_exceptions

    cred = credentials.Certificate("users_service/utils/firebase_keys.json")

    default_app = firebase_admin.initialize_app(cred)


    def create_user(email: str, password: str):
        try:
            user = auth.create_user(email=email, password=password, app=default_app)
        except (ValueError, auth.UserNotFoundError, fb_exceptions.FirebaseError):
            raise exceptions.UserWrongLoginInformation
        else:
            return user.uid

    def valid_user(email):
        try:
            user = auth.get_user_by_email(email,default_app)
        except (ValueError, auth.UserNotFoundError, fb_exceptions.FirebaseError):
            raise exceptions.UserWrongLoginInformation
        else:
            return user.uid

    def delete_user(uid):
        try: 
            auth.delete_user(uid, app=default_app)
        except (ValueError, auth.UserNotFoundError, fb_exceptions.FirebaseError):
            raise exceptions.UserWrongLoginInformation
