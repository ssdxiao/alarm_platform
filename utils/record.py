#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app.database import db


def save_record(user, obj, obj_id, action, context):
    db.save_record(user, obj, int(obj_id), action, context)

