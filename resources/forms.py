from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,IntegerField,RadioField,SelectMultipleField,EmailField,HiddenField
from wtforms.validators import DataRequired,Length,EqualTo
from models import labelmodel

Color_list = [("#FFFFFF","White"),("#F08080","Light Coral"),("#D2B48C","Tan"),("#66CDAA","MediumAquaMarine"),("#FFC0CB","Pink"),("#D8BFD8","Thistle"),("#B0E0E6","PowderBlue")]

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=4,max=20)])
    email = EmailField('Email ID',validators=[DataRequired(),Length(min=4,max=80)])
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
    color = RadioField("Background Colour",choices=Color_list,validators=[])
    labels = SelectMultipleField('Labels', coerce=int,validators=[])
    create = SubmitField('Create')

    def __init__(self, *args, **kwargs):
        super(CreateNoteForm, self).__init__(*args, **kwargs)
        self.labels.choices = [(label.id, label.name) for label in labelmodel.query.filter(
            (labelmodel.is_system_label == True) | (labelmodel.user_id == session['user_id'])).all()]


class ModifyNoteForm(FlaskForm):
    id = HiddenField('Id',validators=[DataRequired()])
    title = StringField('Title',validators=[DataRequired(),Length(min=1,max=100)])
    content = TextAreaField('Content',validators=[DataRequired(),Length(min=1,max=1000)], render_kw={"rows":"13"})
    color = RadioField("Background Colour",choices=Color_list)
    labels = SelectMultipleField('Labels', coerce=int)
    modify = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(ModifyNoteForm, self).__init__(*args, **kwargs)
        self.labels.choices = [(label.id, label.name) for label in labelmodel.query.filter(
            (labelmodel.is_system_label == True) | (labelmodel.user_id == session.get('user_id',''))).all()]
        
class LabelForm(FlaskForm):
    name = StringField('Label Name',validators=[DataRequired(),Length(min=1,max=100)],render_kw={"placeholder": " name your new label"})
    submit = SubmitField('Create')
