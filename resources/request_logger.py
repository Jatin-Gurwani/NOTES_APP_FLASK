from functools import wraps
from flask import request, current_app
import json
import time


def log_request_response(f):
    
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
                body = {k: '******' if k in ['password', 'access_token'] else v 
                       for k, v in body.items()}
        except Exception:
            body = None

        # Log the request
        request_id = str(int(time.time() * 1000))
        current_app.api_logger.info(
            f"API Request {request_id} | "
            f"Host: {host} | "
            f"Method: {method} | "
            f"Endpoint: {endpoint} | "
            f"URL: {url} | "
            #f"Headers: {headers} | "
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