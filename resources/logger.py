import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from flask import request,current_app
from functools import wraps
import json
import time
from config import app_config
cfg = app_config()

def setup_logger(app):

    # Configure Flask logging
    current_time = datetime.now()
    log_file_name = f'NotesApp_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}.log'
    month_folder = current_time.strftime('%Y%m%d')
    log_dir = os.path.join(cfg.LOG_PATH, month_folder)
    os.makedirs(log_dir, exist_ok=True)
    log_dir = os.path.join(log_dir, log_file_name)
    
    log_format = '[%(asctime)s] %(levelname)s in %(module)s >>> %(message)s'
    #file_handler = logging.FileHandler(log_dir)
    file_handler = RotatingFileHandler(log_dir,maxBytes=cfg.LOG_FILE_SIZE,backupCount=cfg.LOG_FILE_COUNT)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    
    # Setup API logger
    api_logger = logging.getLogger('API_Logger')
    api_logger.setLevel(logging.INFO)
    api_logger.addHandler(file_handler)
    api_logger.propagate = False
    
    # Setup Flask app logger
    app.logger.addHandler(file_handler)
    
    return api_logger 


    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Record start time
        start_time = time.time()
        
        # Get request details
        method = request.method
        endpoint = request.endpoint
        url = request.url
        host = request.host
        headers = dict(request.headers)
        
        # Safely get request body
        try:
            body = request.get_json() if request.is_json else dict(request.form)
            # Remove sensitive data
            if body and isinstance(body, dict):
                if 'password' in body:
                    body['password'] = '******'
                if 'access_token' in body:
                    body['access_token'] = '******'
        except Exception:
            body = None

        # Log the request
        request_id = str(int(time.time() * 1000))  # Simple request ID
        current_app.api_logger.info(
            f"API Request {request_id} | "
            f"Host: {host} | "
            f"Method: {method} | "
            f"Endpoint: {endpoint} | "
            f"URL: {url} | "
            f"Headers: {headers} | "
            f"Body: {json.dumps(body) if body else 'No Body'}"
        )

        # Execute the actual function
        try:
            response = f(*args, **kwargs)
            status_code = response.status_code if hasattr(response, 'status_code') else 200
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Log the response
            current_app.api_logger.info(
                f"API Response {request_id} | "
                f"Endpoint: {endpoint} | "
                f"Status: {status_code} | "
                f"Execution Time: {execution_time:.2f}s"
            )
            
            return response
            
        except Exception as e:
            # Log any errors
            current_app.api_logger.error(
                f"API Error {request_id} | "
                f"Endpoint: {endpoint} | "
                f"Error: {str(e)}"
            )
            raise

    return decorated_function