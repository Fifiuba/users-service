class FirebaseMock:
    
    uid= "asdasdasdslwlewed1213123"

    def create_user(self, email, password):
        return self.uid

    def valid_user(self, email):
        return self.uid
    
    def delete_user(self, uid_user):
        pass
