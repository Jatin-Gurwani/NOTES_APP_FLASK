from flask import Flask,render_template,request,jsonify
from flask_smorest import Api
from models import db, usermodel
from resources import blp_api_user,blp_api_notes,blp_api_access
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import app_config

app = Flask(__name__)
cfg =app_config()
app_url_prefix = '/app'

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


@app.route('/')
def introduction():
    return render_template('Home.html')

