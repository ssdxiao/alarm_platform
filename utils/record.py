
from app.database import db


def save_record(user, obj, obj_id, action, context):
    db.save_record(int(user), obj, int(obj_id), action, context)

