from marshmallow import Schema,fields

class api_user_schema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True,load_only=True)

class api_notes_plain_schema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    user_id = fields.Integer(required=True)
    updated_at = fields.DateTime(dump_only=True)

class api_notes_fetch_schema(Schema):
    id = fields.Integer( required = False)
    title = fields.Str(dump_only=True)
    content = fields.Str(dump_only=True)
    user_id = fields.Integer(required=True)
    updated_at = fields.DateTime(dump_only=True)

class api_notes_update_schema(Schema):
    id = fields.Integer(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    user_id = fields.Integer(required=True)
