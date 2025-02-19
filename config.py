from dotenv import load_dotenv
import os

class app_config():
    
    load_dotenv()
    #Default Values Configuration
    default_database_uri = 'sqlite:///data.db'
    default_path = '/logs/'
    default_log_file_size = 10000000
    default_log_file_count = 10

    #Flask SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', default_database_uri)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS','False')

    #Flask Configuration
    PROPAGATE_EXCEPTIONS = os.getenv('PROPAGATE_EXCEPTIONS')
    API_TITLE = os.getenv('API_TITLE')
    API_VERSION = os.getenv('API_VERSION')
    OPENAPI_VERSION = os.getenv('OPENAPI_VERSION')
    OPENAPI_URL_PREFIX = os.getenv('OPENAPI_URL_PREFIX')
    OPENAPI_SWAGGER_UI_PATH= os.getenv('OPENAPI_SWAGGER_UI_PATH')
    OPENAPI_SWAGGER_UI_URL = os.getenv('OPENAPI_SWAGGER_UI_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')

    #Logger Configuration
    LOG_PATH = os.getenv('LOG_PATH',default_path)
    LOG_FILE_SIZE = int(os.getenv('LOG_FILE_SIZE',default_log_file_size))
    LOG_FILE_COUNT = int(os.getenv('LOG_FILE_COUNT',default_log_file_count))

