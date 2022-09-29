from users_service.database import exceptions


class FirebaseMock:

    uid = "asdasdasdslwlewed1213123"
    email = ""
    token = "hfjdshfuidhysvcsbvs83hfsdf"

    def create_user(self, email, password):
        self.email = email
        return self.uid

    def valid_user(self, token):
        if token == self.token:
            return self.uid, self.email
        else:
            raise exceptions.UserWrongLoginInformation

    def delete_user(self, uid_user):
        pass
