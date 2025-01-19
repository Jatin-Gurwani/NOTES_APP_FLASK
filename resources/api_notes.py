from flask import Flask,request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
import werkzeug
from models import notesmodel, db, usermodel
from resources import api_notes_plain_schema,api_notes_fetch_schema,api_notes_update_schema
from datetime import datetime

api_notes_url_prefix = '/api/notes'
blp = Blueprint('API_NOTES',__name__,url_prefix=api_notes_url_prefix,description='Oprations  for notes management')

@blp.route('/create')
class create_notes(MethodView):
    
    @blp.arguments(api_notes_plain_schema)
    def post(self,notes_data):
        try:
            if usermodel.query.filter(usermodel.id == notes_data['user_id']).first():
                current_date_time = datetime.now()
                new_note = notesmodel(title = notes_data["title"],content = notes_data["content"],user_id = notes_data["user_id"],created_at = current_date_time,updated_at = current_date_time)
                db.session.add(new_note)
                db.session.commit()
                return {"message":"Note created successfully"},201
            
            else:
                abort(400, message="User does not exist")
        except IntegrityError as e :
            print("error at api notes create endpoint : ",e)
            abort(400,message="Note already exist")
        except SQLAlchemyError as e:
            print("error at api notes create endpoint : ",e)
            abort(500,message="unable to add note details into backend")
        except Exception as e:
            print("error at api notes create endpoint : ",e)
            abort(500,message="unable to add note details into backend")

@blp.route('/notes_view/<int:id>')
class view_notes_by_id(MethodView):

    @blp.response(200,api_notes_plain_schema)
    def get(self,id):
        try:
            note = notesmodel.query.filter(notesmodel.id == id).first_or_404()
            return note
        except Exception as e:
            print("error at api notes view endpoint : ",e)
            abort(404,message="Note not found")

@blp.route('/user_view/<int:id>')
class view_notes_by_userid(MethodView):

    @blp.response(200,api_notes_plain_schema(many=True))
    def get(self,id):
        try:
            notes_array= notesmodel.query.filter(notesmodel.user_id == id).all()
            return notes_array
        except SQLAlchemyError as e:
            print("error at api notes user view endpoint : ",e)
            abort(404,message="Notes not found")
        except Exception as e:
            print("error at api notes user view endpoint : ",e)
            abort(404,message="Notes not found")

@blp.route('/view')
class view_notes(MethodView):

    @blp.arguments(api_notes_fetch_schema)
    @blp.response(200,api_notes_plain_schema(many=True))
    def post(self,notes_data):
        try:
            if "id" in notes_data:
                notes_array= notesmodel.query.get_or_404(notes_data['id'])
                return [notes_array]
            else:
                notes_array = notesmodel.query.filter(notesmodel.user_id == notes_data['user_id']).all()
                return notes_array
        except SQLAlchemyError as e:
            print("error at api notes view endpoint : ",e)
            abort(404,message="Notes not found")
        except Exception as e:
            print("error at api notes view endpoint : ",e)
            abort(404,message="Notes not found")

@blp.route('/update')
class update_notes(MethodView):

    @blp.arguments(api_notes_update_schema)
    def put(self,notes_data):
        try:
            if notesmodel.query.filter(notesmodel.id == notes_data['id']).filter(notesmodel.user_id == notes_data['user_id']).first_or_404():
                current_date_time = datetime.now()
                notesmodel.query.filter(notesmodel.id == notes_data['id']).update({"title":notes_data["title"],"content":notes_data["content"],"updated_at":current_date_time})
                db.session.commit()
                return {"message":"Note updated successfully"},201
            else:
                abort(400,message="Note does not exist or not assoiated with user")
        except IntegrityError as e :
            print("error at api notes update endpoint : ",e)
            abort(400,message=" invalid note id")
        except SQLAlchemyError as e:
            print("error at api notes update endpoint : ",e)
            abort(500,message="unable to update note details into backend")
        except werkzeug.exceptions.NotFound as e:
            print("error at api notes update endpoint : ",e)
            abort(404,message="Note not found or not associated with user")
        except Exception as e:
            print("error at api notes update endpoint : ",e)
            abort(500,message="unable to update note details into backend")

@blp.route('/delete/<int:id>')
class delete_notes(MethodView):

    def delete(self,id):
        try:
            notesmodel.query.filter(notesmodel.id == id).delete()
            db.session.commit()
            return {"message":"Note deleted successfully"},200
        except Exception as e:
            print("error at api notes delete endpoint : ",e)
            abort(404,message="Note not found")