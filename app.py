from flask import Flask,render_template,request,jsonify
from flask_smorest import Api
from models import db, usermodel
from resources import blp_api_user,blp_api_notes,blp_api_access
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app_url_prefix = '/app'
db_url= "oracle+oracledb://NOTES_FLASK_APP:admin_user@localhost:1521/?service_name=freepdb1"

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Notes REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/apidocs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"]= db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



db.init_app(app)
migrate=Migrate(app,db)


app.config["JWT_SECRET_KEY"] = "Notes Flask App"
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

