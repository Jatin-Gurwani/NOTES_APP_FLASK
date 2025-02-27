
# Notes APP

Built a personal notes application with Flask, providing users with a secure and convenient way to manage their notes.The application features:

* User-friendly interface for creating, editing, and deleting notes.

* Note organization with labels and colours.

* Data persistence using Oracle Database.

* Implemented using Flask framework, demonstrating skills in routing, templating, and database integration.


## Tech Stack

* **Flask**: The core framework used to build the web application.

* **Flask-Smorest**: Used for building REST APIs with Flask.

* **Python-dotenv**: For managing environment variables.

* **Marshmallow**: An object serialization/deserialization library.

* **SQLAlchemy**: An ORM (Object Relational Mapper) for database interactions.

* **Flask-SQLAlchemy**: Integration of SQLAlchemy with Flask.

* **OracleDB**: Database used for storing data.

* **Passlib**: For password hashing.

* **Flask-Migrate**: For handling database migrations.

* **Flask-JWT-Extended**: For handling JSON Web Tokens (JWT) for authentication.

* **Flask-WTF**: For handling forms in Flask.

* **Bootstrap-Flask**: To integrate Bootstrap with Flask for responsive UI.
##  Application Features

- Create,Edit and Delete Personal Notes.
- Pin and Unpin Note.
- Personalize note with different colours.
- Search Notes.
- Create , Delete Custom Labels.
- Manage Notes with different labels.
- Intregrate Notes with Thrid Party Application Using API.
## Running in Local
- Clone the Repository
- Create virtual environment

   ```bash 
    python -m venv .venv
   ```
- Activate  virtual environment

    ```bash 
    .venv\Scripts\activate.bat
    ```   
- Install Packages 

    ```bash
     pip install -r requirements.txt
    ```
- create .env file 
    
    refer [.sample_env](https://github.com/Jatin-Gurwani/NOTES_APP_FLASK/blob/main/.sample_env)
- Create Application Tables in Oracle Database
    ```python 
    from app import app,db
    with app.app_context():
    db.create_all()
    ```
- Run Application
    ```bash
    flask run
    ```
