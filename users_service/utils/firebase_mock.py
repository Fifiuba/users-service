from users_service.database import exceptions


class FirebaseMock:
    usersfireabse = {}
    usersfireabse["hfjdshfuidhysvcsbvs83hfsdf"] = {
        "uid": "asdasdasdslwlewed1213123",
        "email": "agus@gmail.com",
        "name": "agus",
        "picture": "picture",
    }
    usersfireabse["ahsgdhauiwhfdiwhf"] = {
        "uid": "djdhdhdhd",
        "email": "sol@gmail.com",
        "name": "sol",
        "picture": "picture"
    }
    usersfireabse["eujthfydhd"] = {
        "uid": "shdashdHSDY",
        "email": "ale@gmail.com",
        "name": "ale",
        "picture": "picture"
    }


    def create_user(self, email, password):
        uid = None
        for value in self.usersfireabse.values():
            print(value)
            if value['email'] == email:
                uid = value['uid']
        return uid


    def valid_user(self, token):
        if token in self.usersfireabse.keys():
            return self.usersfireabse[token]
        else:
            raise exceptions.UserWrongLoginInformation

    def get_email(self, uid):
        email = None
        for value in self.usersfireabse.values():
            print(value)
            if value['uid'] == uid:
                email = value['email']
        return email

    def delete_user(self, uid_user):
        pass
