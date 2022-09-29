from firebase_admin import exceptions as fb_exceptions
from users_service.database import exceptions


class Firebase:
    def __init__(self, auth, app):
        self.auth = auth
        self.app = app

    def create_user(self, email: str, password: str):
        try:
            user = self.auth.create_user(email=email, password=password, app=self.app)
        except (ValueError, self.auth.UserNotFoundError, fb_exceptions.FirebaseError):
            raise exceptions.UserWrongLoginInformation
        else:
            return user.uid

    def valid_user(self, token):
        try:
            user = self.auth.verify_id_token(token, app=self.app)

        except (
            self.auth.UserDisabledError,
            self.auth.CertificateFetchError,
            self.auth.RevokedIdTokenError,
            self.auth.ExpiredIdTokenError,
            self.auth.InvalidIdTokenError,
        ):

            raise exceptions.UserWrongLoginInformation
        else:
            return user.get("uid"), user.get("email")

    def delete_user(self, uid):
        try:
            self.auth.delete_user(uid, app=self.app)
        except (ValueError, self.auth.UserNotFoundError, fb_exceptions.FirebaseError):
            raise exceptions.UserWrongLoginInformation
