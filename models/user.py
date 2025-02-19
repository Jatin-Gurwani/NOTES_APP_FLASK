from models import db


class usermodel(db.Model):
    __tablename__ = 'TBL_NOTES_APP_USERS'



    id_seq = db.Sequence('notes_app_users_id_seq')
    id = db.Column(db.Integer ,id_seq,server_default=id_seq.next_value(),primary_key=True)
    username = db.Column(db.String(256), unique=True,nullable=False )
    email = db.Column(db.String(256), unique=True,nullable=False )
    password = db.Column(db.String(256),nullable=False)
    notes = db.relationship("notesmodel", back_populates="user",lazy="dynamic",cascade="all, delete")
    labels = db.relationship("labelmodel", back_populates="user",lazy="dynamic",cascade="all, delete")

