from models import db


class notesmodel(db.Model):
    __tablename__ = 'TBL_NOTES_APP_NOTES'

    id_seq = db.Sequence('notes_app_notes_id_seq')
    id = db.Column(db.Integer,id_seq,server_default=id_seq.next_value(),primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    content = db.Column(db.String(256),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('TBL_NOTES_APP_USERS.id'),nullable=False)
    created_at = db.Column(db.DATE(),nullable=False)
    updated_at = db.Column(db.DATE(),nullable=False)
    user = db.relationship('usermodel', back_populates='notes')