from flask import Flask,render_template,request
from flask_smorest import Api
from models import db, usermodel
from resources import blp_api_user,blp_api_notes
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

app = Flask(__name__)
app_url_prefix = '/app'
db_url= "oracle+oracledb://ot:yourpassword@localhost:1521/?service_name=freepdb1"

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

with app.app_context():
        db.create_all()

API = Api(app)
API.register_blueprint(blp_api_user)
API.register_blueprint(blp_api_notes)


@app.route('/')
def introduction():
    return render_template('Home.html')

