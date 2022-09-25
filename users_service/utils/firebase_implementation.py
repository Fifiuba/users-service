from firebase_admin import exceptions as fb_exceptions
from users_service.database import exceptions

class Firebase():
    def __init__(self,auth,app):
        self.auth = auth
        self.app = app

    def create_user(self, email: str, password: str):
        try:
            user = self.auth.create_user(email=email, password=password, app=self.app)
        except (ValueError, self.auth.UserNotFoundError, fb_exceptions.FirebaseError):
            raise exceptions.UserWrongLoginInformation
        else:
            return user.uid

    def valid_user(self, email):
        try:
            user = self.auth.get_user_by_email(email,self.app)
        except (ValueError, self.auth.UserNotFoundError, fb_exceptions.FirebaseError):
            raise exceptions.UserWrongLoginInformation
        else:
            return user.uid

    def delete_user(self, uid):
        try: 
            self.auth.delete_user(uid, app=self.app)
        except (ValueError, self.auth.UserNotFoundError, fb_exceptions.FirebaseError):
            raise exceptions.UserWrongLoginInformation