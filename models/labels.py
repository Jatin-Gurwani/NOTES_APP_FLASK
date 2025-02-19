from models import db

class labelmodel(db.Model):
    
    __tablename__ = 'TBL_NOTES_APP_LABELS'

    id_seq = db.Sequence('notes_app_labels_id_seq')
    id = db.Column(db.Integer,id_seq,server_default=id_seq.next_value(),primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    is_system_label = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('TBL_NOTES_APP_USERS.id'), nullable=True)
    user = db.relationship('usermodel', back_populates='labels')
    

