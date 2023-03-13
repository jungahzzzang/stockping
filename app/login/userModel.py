from flask_login import UserMixin
from db import get_db
class User(UserMixin):
    def __init__(self, user):
        self.id = str(user['_id'])
        self.username = user['username']

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.users.find_one({'_id': ObjectId(user_id)})
       
