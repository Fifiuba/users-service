from users_service.database import exceptions


class FirebaseMock:
    usersfireabse = {}
    usersfireabse["hfjdshfuidhysvcsbvs83hfsdf"] = {
        "uid": "asdasdasdslwlewed1213123",
        "email": "agus@gmail.com",
        "name": "agus",
        "picture": "picture",
        "block": False,
    }
    usersfireabse["ahsgdhauiwhfdiwhf"] = {
        "uid": "djdhdhdhd",
        "email": "sol@gmail.com",
        "name": "sol",
        "picture": "picture",
        "block": False,
    }
    usersfireabse["eujthfydhd"] = {
        "uid": "shdashdHSDY",
        "email": "ale@gmail.com",
        "name": "ale",
        "picture": "picture",
        "block": False,
    }
    usersfireabse["ueywepd"] = {
        "uid": "poiyres",
        "email": "franco@gmail.com",
        "name": "franco",
        "picture": "picture",
        "block": False,
    }

    def create_user(self, email, password):
        uid = None
        for value in self.usersfireabse.values():
            if value["email"] == email:
                uid = value["uid"]
        return uid

    def valid_user(self, token):
        info = None
        if token in self.usersfireabse.keys():
            info = self.usersfireabse[token]
            if info["block"]:
                raise exceptions.UserIsBlock
            else:
                return info
        else:
            raise exceptions.UserWrongLoginInformation

    def get_email(self, uid):
        email = None
        for value in self.usersfireabse.values():
            if value["uid"] == uid:
                email = value["email"]
        return email

    def delete_user(self, uid_user):
        pass

    def block_user(self, uid, block):
        for value in self.usersfireabse.values():
            if value["uid"] == uid:
                value["block"] = block
