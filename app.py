from flask import Flask,render_template,request,jsonify,session,redirect,url_for
from flask_bootstrap import Bootstrap5
from flask_smorest import Api
from flask_wtf import CSRFProtect
from models import db, usermodel
from resources import blp_api_user,blp_api_notes,blp_api_access,blp_app_user,blp_app_notes
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import app_config
import urllib.parse
from resources.logger import setup_logger
from resources.request_logger import log_request_response

app = Flask(__name__)
cfg = app_config()
app_url_prefix = '/app'

# Setup logging
app.api_logger = setup_logger(app)
app.logger.info("Flask is getting Started")

app.config["PROPAGATE_EXCEPTIONS"] = cfg.PROPAGATE_EXCEPTIONS
app.config["API_TITLE"] = cfg.API_TITLE
app.config["API_VERSION"] = cfg.API_VERSION
app.config["OPENAPI_VERSION"] = cfg.OPENAPI_VERSION
app.config["OPENAPI_URL_PREFIX"] = cfg.OPENAPI_URL_PREFIX
app.config["OPENAPI_SWAGGER_UI_PATH"] = cfg.OPENAPI_SWAGGER_UI_PATH
app.config["OPENAPI_SWAGGER_UI_URL"] = cfg.OPENAPI_SWAGGER_UI_URL
app.config["SQLALCHEMY_DATABASE_URI"]= cfg.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = cfg.SQLALCHEMY_TRACK_MODIFICATIONS



db.init_app(app)
migrate=Migrate(app,db)


app.config["JWT_SECRET_KEY"] = cfg.JWT_SECRET_KEY


bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = cfg.SECRET_KEY
jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )
    

API = Api(app)
API.register_blueprint(blp_api_user)
API.register_blueprint(blp_api_notes)
API.register_blueprint(blp_api_access)
API.register_blueprint(blp_app_user,url_prefix = '/')
API.register_blueprint(blp_app_notes,url_prefix = '/app')

@app.errorhandler(404)
def page_not_found(e = None):
    app.api_logger.error(f'endpoint : {request.url}, message : {e}')
    if request.path.startswith('/api/'):
         return jsonify({"status": "Not Found","code": 404}),404
    else:
        return render_template('404.html'),404

@app.errorhandler(405)
def method_not_found(e = None):
    if request.path.startswith('/api/'):
         return jsonify({"status": "Method Not Allowed","code": 405}),405
    else:
        return render_template('404.html'),405

@app.errorhandler(500)
def Internal_server_error(e = None,message = "Internal server error"):
    if request.path.startswith('/api/'):
         return jsonify({"status": "internal server error","code": 500 , "message":message}),500
    else:
        if e is not None:
            print("Error 500 : ",e)
        return render_template('500.html'),500
    
@app.template_filter('quote')
def quote_filter(s):
     return urllib.parse.quote(s)

@app.template_filter('summary')
def content_summary(s):
    return  s if len(s) < 150 else s[0:150] + '....'
