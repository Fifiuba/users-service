from firebase_admin import exceptions as fb_exceptions
from users_service.database import exceptions


class Firebase:
    def __init__(self, auth, app):
        self.auth = auth
        self.app = app

    def create_user(self, email: str, password: str):
        try:
            user = self.auth.create_user(email=email, password=password, app=self.app)
        except (ValueError, self.auth.UserNotFoundError, fb_exceptions.FirebaseError) as error:
            print(error)
            raise exceptions.UserWrongLoginInformation
        else:
            return user.uid

    def get_email(self, uid: str):
        user = self.auth.get_user(uid, app=self.app)
        email = user.__dict__['_data']['providerUserInfo'][0]['email']
        return email

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
            print("entre aca")
            print("toy en firebase ", user)
            return user

    def delete_user(self, uid):
        try:
            self.auth.delete_user(uid, app=self.app)
        except (ValueError, self.auth.UserNotFoundError, fb_exceptions.FirebaseError):
            raise exceptions.UserWrongLoginInformation
