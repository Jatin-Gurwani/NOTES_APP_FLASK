from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Length,EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    register = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
    login = SubmitField('Login')

class SearchForm(FlaskForm):
    search = StringField('search',render_kw={"placeholder": "Search anything"})
    search_submit = SubmitField('search')

class CreateNoteForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(min=1,max=100)])
    content = TextAreaField('Content',validators=[DataRequired(),Length(min=1,max=1000)],render_kw={"rows":"10"})
    create = SubmitField('Create')

class ModifyNoteForm(FlaskForm):
    id = IntegerField('Id',validators=[DataRequired()])
    title = StringField('Title',validators=[DataRequired(),Length(min=1,max=100)])
    content = TextAreaField('Content',validators=[DataRequired(),Length(min=1,max=1000)], render_kw={"rows":"13"})
    modify = SubmitField('Save')
