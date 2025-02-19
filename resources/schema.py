from marshmallow import Schema,fields

# response schema
class api_response_schema(Schema):
    message = fields.Str(dump_only=True)
    status = fields.Str(dump_only=True)

# api/user schema
class api_user_schema(api_response_schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True,load_only=True)

class api_user_register_schema(api_response_schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True,load_only=True)

# api/notes schema
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

class api_notes_response_schema(api_response_schema):
    notes = fields.List(fields.Nested(api_notes_plain_schema()),dump_only=True)

#api/access schema
class api_access_plain_schema(api_response_schema):
    username= fields.Str(required=True,load_only=True)
    source = fields.Str(required=True,load_only=True)
    access_token = fields.Str(dump_only=True)

class api_access_register_schema(api_response_schema):
    username = fields.Str(required=True,load_only=True)
    source = fields.Str(required=True,load_only=True)
    client_name = fields.Str(required=True,load_only=True)