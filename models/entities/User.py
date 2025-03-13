from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_user, username, password, mail=""):
        self.id = id_user
        self.username = username
        self.password = password
        self.mail = mail 

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)