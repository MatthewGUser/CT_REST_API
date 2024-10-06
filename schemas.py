# schemas.py
from marshmallow import Schema, fields

class MemberSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)

class WorkoutSessionSchema(Schema):
    id = fields.Int(dump_only=True)
    member_id = fields.Int(required=True)
    session_date = fields.DateTime(required=True)
    duration = fields.Int(required=True)
