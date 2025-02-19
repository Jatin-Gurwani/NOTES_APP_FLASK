from flask import Flask,request,current_app
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from models import db, api_access_model
from resources import api_access_plain_schema,api_access_register_schema
from flask_jwt_extended import jwt_required,create_access_token
from datetime import datetime
from resources.request_logger import log_request_response

api_access_url_prefix = '/api/access'
blp = Blueprint('API_ACCESS',__name__,url_prefix=api_access_url_prefix,description='Oprations for api access management')

@blp.route('/login')
class create_user_access_token(MethodView):

    @blp.arguments(api_access_plain_schema)
    @blp.response(200,api_access_plain_schema)
    @log_request_response
    def post(self,login_data):
        try:
            user = api_access_model.query.filter(api_access_model.username == login_data['username'] and api_access_model.source == login_data['source']).first()
            if user:
                if user.is_locked == 'Y':
                    current_app.api_logger.warning(f"Login attempt for locked user: {login_data['username']} from source: {login_data['source']}")
                    abort(403,message="User is locked")
                else:
                    access_token = create_access_token(identity=str(user.id))
                    current_app.api_logger.info(f"Access token generated for user: {login_data['username']} from source: {login_data['source']}")
                    response_data = {"access_token":access_token,"message":"Access token generated successfully","status":"Success"}
                    return response_data
            else:
                current_app.api_logger.warning(f"Invalid login attempt - username: {login_data['username']}, source: {login_data['source']}")
                abort(404,message="Username or Source is not valid")
        except SQLAlchemyError as e:
            current_app.api_logger.error(f"SQLAlchemyError in create_user_access_token: {e}")
            abort(500, message="Internal Server Error")
        except Exception as e:
            current_app.api_logger.error(f"Unexpected error in create_user_access_token: {e}")
            abort(500, message="Internal Server Error")

@blp.route('/register')
class create_api_account(MethodView):
    
    @blp.arguments(api_access_register_schema)
    @blp.response(201,api_access_register_schema)
    @log_request_response
    def post(self,register_data):
        try:
            if api_access_model.query.filter(api_access_model.username == register_data['username'] and api_access_model.source == register_data['source']).first():
                current_app.api_logger.warning(f"Registration failed - User already exists: {register_data['username']} from source: {register_data['source']}")
                abort(409,message="User already exists")
            else:
                new_user = api_access_model(username=register_data['username'],source=register_data['source'],client_name=register_data['client_name'],is_locked='N',created_at=datetime.now())
                db.session.add(new_user)
                db.session.commit()
                current_app.api_logger.info(f"New API user registered successfully: {register_data['username']} from source: {register_data['source']}")
                response_data={"message":"User registered successfully","status":"Success"}
                return response_data
        except IntegrityError as e:
            current_app.api_logger.error(f"IntegrityError in api_access register: {e}")
            abort(409,message="User already exists")
        except SQLAlchemyError as e:
            current_app.api_logger.error(f"SQLAlchemyError in api_access register: {e}")
            abort(500, message="Unable to register user due to some technical issue")  
        
