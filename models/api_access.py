from models import db

class api_access_model(db.Model):
    __tablename__ = 'TBL_NOTES_APP_API_ACCESS'

    id_seq = db.Sequence('notes_app_api_access_id_seq')
    id = db.Column(db.Integer,id_seq,server_default=id_seq.next_value(),primary_key=True)
    client_name = db.Column(db.String(80),nullable=False)
    username = db.Column(db.String(80),nullable=False)
    source = db.Column(db.String(80),nullable=False)
    is_locked = db.Column(db.String(1),nullable=False)
    created_at = db.Column(db.DATE(),nullable=False)