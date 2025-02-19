from flask import Flask,render_template,redirect,url_for,session,request,flash,current_app
from flask.views import MethodView
from models import db,usermodel
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from resources.forms import RegisterForm,LoginForm


blp = Blueprint('APP_USER',__name__,template_folder='templates' ,description='User Management Operations for Web Interface')

@blp.route('/')
class app_home(MethodView):
    def get(self):
        try:
            if session['user_logged_in']:
                flash('Welcome Back ', 'info')
                return redirect(url_for('APP_NOTES.all_notes'))
            return render_template('home.html')
        except Exception as e:
            return render_template('home.html')
    
@blp.route('/register')
class app_register(MethodView):

    
    def get(self):
        form = RegisterForm()
        return render_template('register.html',form= form)
    
    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            user = usermodel.query.filter(usermodel.username == username).first()
            if user:
                return render_template('register.html',error="User Already Exist")
            else:
                try:
                    user_password_encrypted = pbkdf2_sha256.hash(password)
                    new_user = usermodel(username = username,password = user_password_encrypted,email = email)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('User Registered Successfully', 'info')
                    return redirect(url_for('APP_USER.app_login'))
                except IntegrityError as e:
                    flash('User already exist', 'error')
                    return render_template('register.html',error="User Already Exist",form= form)
                except SQLAlchemyError as e:
                    flash('Your request has been failed , please try again later', 'error')
                    return render_template('register.html',error="unable to add user details into backend",form= form)
                except Exception as e:
                    return render_template('register.html',error="unable to add user details into backend",form= form)
        else:
            return render_template('register.html',form= form)
    
@blp.route('/login')
class app_login(MethodView):
    def get(self):
        form = LoginForm()
        return render_template('login.html',form= form)
    
    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']
            user = usermodel.query.filter(usermodel.username == username).first()
            if user and pbkdf2_sha256.verify(password, user.password):
                session['user_logged_in']=True
                session['user_name']=username
                session['user_id']=user.id
                flash('you are logged in  successfully', 'info')
                return redirect(url_for('APP_NOTES.all_notes'))
            else:
                flash('Invalid username or password', 'error')
                return render_template('login.html',form= form)
        else:
            flash('Your request has been failed , please try again later', 'error')
            return render_template('login.html',form= form)
        
@blp.route('/logout')
class app_logout(MethodView):
    def get(self):
        session.clear()
        flash('You have been Logged out Successfully', 'info')
        return redirect(url_for('APP_USER.app_home'))
    
    
        

    