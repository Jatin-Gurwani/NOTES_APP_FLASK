from flask import Flask,request, current_app
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from passlib.hash import pbkdf2_sha256
from models import db, usermodel
from resources import api_user_schema,api_response_schema,api_user_register_schema
from flask_jwt_extended import jwt_required
from resources.request_logger import log_request_response

api_user_url_prefix = '/api/user'
blp = Blueprint('API_USER',__name__,url_prefix=api_user_url_prefix,description='Oprations for user management')


@blp.route('/register')
class CreateUser(MethodView):

    @blp.arguments(api_user_register_schema)
    @blp.response(201,api_response_schema)
    @jwt_required()
    @log_request_response
    def post(self,User_Data):
        if usermodel.query.filter(usermodel.username == User_Data['username']).first():
                current_app.api_logger.warning(f"User registration failed - Username already exists: {User_Data['username']}")
                abort(409,message="User Already Exist")
        else:
            try:
                user_password_encrypted = pbkdf2_sha256.hash(User_Data["password"])
                new_user = usermodel(username = User_Data["username"],password = user_password_encrypted,email = User_Data["email"])
                db.session.add(new_user)
                db.session.commit()
                current_app.api_logger.info(f"New user registered successfully: {User_Data['username']}")
                response_data = {"message":"User created successfully","status":"Success"}
                return response_data
            except IntegrityError as e:
                current_app.api_logger.error(f"IntegrityError in user register: {e}")
                abort(400,message="User already exist")
            except SQLAlchemyError as e:
                current_app.api_logger.error(f"SQLAlchemyError in user register: {e}")
                abort(500,message="unable to add user details into backend")
            except Exception as e:
                current_app.api_logger.error(f"Unexpected error in user register: {e}")
                abort(500,message="unable to add user details into backend")

@blp.route('/validate')
class User_Validate(MethodView):
     
    @blp.arguments(api_user_schema)
    @blp.response(200,api_user_schema)
    @jwt_required() 
    @log_request_response
    def post(self,validate_data):
        user = usermodel.query.filter(usermodel.username == validate_data["username"]).first()
        try:
            if user and pbkdf2_sha256.verify(validate_data["password"], user.password):
                current_app.api_logger.info(f"User validated successfully: {validate_data['username']}")
                response_data = {"id": user.id,"username": user.username,"password": user.password}
                response_data["message"] = "User validated successfully"
                response_data["status"] = "Success"
                return response_data
            else:
                current_app.api_logger.warning(f"Invalid login attempt for username: {validate_data['username']}")
                abort(401,message="Invalid username or password")
        except Exception as e:
            current_app.api_logger.error(f"Error in user validate: {e}")
            abort(401,message="Invalid username or password")
            