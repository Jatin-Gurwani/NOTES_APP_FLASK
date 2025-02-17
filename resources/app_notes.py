from flask import Flask,render_template,redirect,url_for,session,request,flash,abort
from flask.views import MethodView
from models import db,notesmodel
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from resources.forms import CreateNoteForm,ModifyNoteForm,SearchForm
from datetime import datetime

blp = Blueprint('APP_NOTES',__name__,template_folder='templates' ,description='Notes Management Operations for Web Interface')


@blp.route('/')
class all_notes(MethodView):
    def get(self):
        try:
            if session['user_id']:
                form = CreateNoteForm()
                modify_form = ModifyNoteForm()
                search_form = SearchForm()
                notes = notesmodel.query.filter(notesmodel.user_id==session['user_id']).all()
                if notes:
                    return render_template('notes.html',note_list=notes,create_form=form,modify_form=modify_form,search_form=search_form)
                else:
                    return render_template('notes.html',notes_message="No Notes To Show",create_form=form,modify_form=modify_form,search_form=search_form)
            else:
                return redirect(url_for('APP_USER.app_logout'))
        except Exception as e:
            abort(500,e)
    
    def post(self):
        try:
            form = CreateNoteForm()
            modify_form = ModifyNoteForm()
            search_form = SearchForm()
            if search_form.validate_on_submit():
                search_str = search_form.search.data
                notes = notesmodel.query.filter( notesmodel.user_id==session['user_id'], ( notesmodel.title.like('%'+search_str+'%') | notesmodel.content.like('%'+search_str+'%'))).all()
                if notes:
                    return render_template('notes.html',note_list=notes,create_form=form,modify_form=modify_form,search_form=search_form)
                else:
                    return render_template('notes.html',notes_message="No Notes To Show",create_form=form,modify_form=modify_form,search_form=search_form)
            else:
                flash('Your request has been failed , please try again later', 'error')
                return redirect(url_for('APP_NOTES.all_notes'))
        except Exception as e:
            abort(500,e)

@blp.route('/create')
class create_note(MethodView):
    
    def post(self):
        try:
            form = CreateNoteForm()
            if form.validate_on_submit():
                form_title = form.title.data
                form_content = form.content.data
                form_user_id = session['user_id']
                curent_time = datetime.now()
                new_note = notesmodel(title=form_title,content=form_content,user_id=form_user_id,created_at=curent_time,updated_at=curent_time)
                db.session.add(new_note)
                db.session.commit()
                flash('New Note Has Been Created', 'info')
                return redirect(url_for('APP_NOTES.all_notes'))
            else:
                return render_template('notes.html',create_form=form)
        except Exception as e:
            abort(500,e)

@blp.route('/modify')
class modify_note(MethodView):

    def post(self):
        try:
            form = ModifyNoteForm()
            form_id = request.form['id']
            form_title = request.form['title']
            form_content = request.form['content']
            curent_time = datetime.now()
            notesmodel.query.filter(notesmodel.id==form_id).update(dict(title=form_title,content=form_content,updated_at=curent_time))
            db.session.commit()
            flash('New Changes have been Saved Successfully', 'info')
            return redirect(url_for('APP_NOTES.all_notes'))
        except Exception as e:
            flash('Your request has been failed , please try again later', 'error')
            return redirect(url_for('APP_NOTES.all_notes'))
        
@blp.route('/delete/<int:id>')
class delete_note(MethodView):
    def get(self,id):
        try:
            note = notesmodel.query.filter(notesmodel.id==id).first()
            if note.user_id == session['user_id']:
                db.session.delete(note)
                db.session.commit()
                flash('Note have been Deleted successfully', 'info')
                return redirect(url_for('APP_NOTES.all_notes'))
        except Exception as e:
            flash('Your request has been failed , please try again later', 'error')
            return redirect(url_for('APP_NOTES.all_notes'))