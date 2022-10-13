from users_service.database import exceptions


class FirebaseMock:
    user = {
        "uid": "asdasdasdslwlewed1213123",
        "email": "agus@gmail.com",
        "name": "agus",
    }

    token = "hfjdshfuidhysvcsbvs83hfsdf"

    def create_user(self, email, password):
        self.user["email"] = email
        return self.user["uid"]

    def valid_user(self, token):
        if token == self.token:
            return self.user
        else:
            raise exceptions.UserWrongLoginInformation
    def get_email(self, uid):
        return self.user['email']
    def delete_user(self, uid_user):
        pass
