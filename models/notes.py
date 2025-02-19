from models import db

notes_labels = db.Table('TBL_NOTES_APP_NOTES_LABELS',
    db.Column('note_id', db.Integer, db.ForeignKey('TBL_NOTES_APP_NOTES.id'), primary_key=True),
    db.Column('label_id', db.Integer, db.ForeignKey('TBL_NOTES_APP_LABELS.id'), primary_key=True)
)

class notesmodel(db.Model):
    __tablename__ = 'TBL_NOTES_APP_NOTES'


    id_seq = db.Sequence('notes_app_notes_id_seq')
    id = db.Column(db.Integer,id_seq,server_default=id_seq.next_value(),primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    content = db.Column(db.String(2048),nullable=False)
    colour = db.Column(db.String(7),nullable=False,default="#FFFFFF")
    is_pinned = db.Column(db.String(1))
    user_id = db.Column(db.Integer, db.ForeignKey('TBL_NOTES_APP_USERS.id'),nullable=False)
    created_at = db.Column(db.DATE(),nullable=False)
    updated_at = db.Column(db.DATE(),nullable=False)
    user = db.relationship('usermodel', back_populates='notes')
    labels = db.relationship('labelmodel', secondary=notes_labels, lazy='subquery', backref=db.backref('notes', lazy=True))