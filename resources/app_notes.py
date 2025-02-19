from flask import Flask,render_template,redirect,url_for,session,request,flash,abort
from flask.views import MethodView
from models import db,notesmodel,labelmodel
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from resources.forms import CreateNoteForm,ModifyNoteForm,SearchForm,LabelForm
from datetime import datetime
from sqlalchemy import text
blp = Blueprint('APP_NOTES',__name__,template_folder='templates' ,description='Notes Management Operations for Web Interface')


@blp.route('/')
class all_notes(MethodView):
    def get(self):
        try:
            if session['user_id']:
                form = CreateNoteForm()
                modify_form = ModifyNoteForm()
                search_form = SearchForm()
                user_labels =  labelmodel.query.filter((labelmodel.is_system_label == True) | (labelmodel.user_id == session['user_id'])).all()
                notes = notesmodel.query.filter(notesmodel.user_id==session['user_id'] ).order_by(notesmodel.is_pinned.desc(),notesmodel.updated_at.desc()).all()
                if notes:
                    return render_template('notes.html',note_list=notes,create_form=form,modify_form=modify_form,search_form=search_form,label_list = user_labels)
                else:
                    return render_template('notes.html',notes_message="No Notes To Show",create_form=form,modify_form=modify_form,search_form=search_form,label_list = user_labels)
            else:
                return redirect(url_for('APP_USER.app_logout'))
        except Exception as e:
            abort(500,e)
    
    def post(self):
        try:
            form = CreateNoteForm()
            modify_form = ModifyNoteForm()
            search_form = SearchForm()
            user_labels =  labelmodel.query.filter((labelmodel.is_system_label == True) | (labelmodel.user_id == session['user_id'])).all()
            if search_form.validate_on_submit():
                search_str = search_form.search.data
                notes = notesmodel.query.filter( notesmodel.user_id==session['user_id'], ( notesmodel.title.like('%'+search_str+'%') | notesmodel.content.like('%'+search_str+'%'))).order_by(notesmodel.is_pinned.desc(),notesmodel.updated_at.desc()).all()
                if notes:
                    return render_template('notes.html',note_list=notes,create_form=form,modify_form=modify_form,search_form=search_form,label_list = user_labels)
                else:
                    return render_template('notes.html',notes_message="No Notes To Show",create_form=form,modify_form=modify_form,search_form=search_form,label_list = user_labels)
            else:
                flash('Your request has been failed , please try again later', 'error')
                return redirect(url_for('APP_NOTES.all_notes'))
        except Exception as e:
            abort(500,e)

@blp.route('/create')
class create_note(MethodView):
    
    def post(self):
        try:
            print(request.referrer)
            form = CreateNoteForm()
            if form.is_submitted():
                form_title = form.title.data
                form_content = form.content.data
                form_user_id = session['user_id']
                form_colour = form.color.data
                labels = labelmodel.query.filter(labelmodel.id.in_(form.labels.data)).all() if form.labels.data else []
                curent_time = datetime.now()
                new_note = notesmodel(title=form_title,content=form_content,user_id=form_user_id,colour=form_colour,labels=labels,created_at=curent_time,updated_at=curent_time,is_pinned='N')
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
            note = notesmodel.query.get_or_404(form_id)
            form_title = request.form['title']
            form_content = request.form['content']
            form_colour = request.form.get('color',note.colour)
            labels = labelmodel.query.filter(labelmodel.id.in_(form.labels.data)).all() if form.labels.data else []
            curent_time = datetime.now()
            note.labels = labels
            notesmodel.query.filter(notesmodel.id==form_id).update(dict(title=form_title,content=form_content,updated_at=curent_time,colour=form_colour))
            db.session.commit()
            flash('New Changes have been Saved Successfully', 'info')
            return redirect(url_for('APP_NOTES.all_notes'))
        except SQLAlchemyError as e:
            print(e)
            abort(500)
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
        
    
@blp.route('/<int:note_id>')
class view_note(MethodView):

    def get(self,note_id):
        note = notesmodel.query.get_or_404(note_id)
        form = CreateNoteForm()
        modify_form = ModifyNoteForm(obj=note)
        user_labels =  labelmodel.query.filter((labelmodel.is_system_label == True) | (labelmodel.user_id == session['user_id'])).all()
        modify_form.color.data = note.colour
        modify_form.labels.data= [label.id for label in note.labels]
        return render_template('notes.html',single_note = note,create_form=form,modify_form=modify_form,label_list = user_labels)
    
@blp.route('/pin/<int:note_id>')
class pin_note(MethodView):

    def get(self,note_id):
        note = notesmodel.query.get_or_404(note_id)
        note.is_pinned = 'N' if note.is_pinned == 'Y' else 'Y'
        print(note.is_pinned)
        db.session.commit()
        return redirect(request.referrer or url_for('APP_NOTES.all_notes'))

@blp.route('/view/pinned')
class pinned_notes(MethodView):
    
    def get(self):
        notelist = notesmodel.query.filter(notesmodel.user_id == session['user_id'],notesmodel.is_pinned == 'Y').order_by(notesmodel.updated_at.desc()).all()
        form = CreateNoteForm()
        search_form = SearchForm()
        user_labels =  labelmodel.query.filter((labelmodel.is_system_label == True) | (labelmodel.user_id == session['user_id'])).all()
        if notelist:
            return render_template('notes.html',note_list=notelist,notes_message="No Notes To Show",create_form=form,search_form=search_form,label_list = user_labels)
        else:
            return render_template('notes.html',notes_message="No Notes To Show",create_form=form,search_form=search_form,label_list = user_labels)

@blp.route('/view/bylabel/<int:label_id>')
class notes_by_label(MethodView):
    
    def get(self,label_id):
        
        query = text('SELECT NOTE_ID FROM TBL_NOTES_APP_NOTES_LABELS WHERE LABEL_ID = :label_id')
        result = db.session.execute(query, {'label_id': label_id})
        rw_note_data = [row[0] for row in result]
        
        notelist = notesmodel.query.filter(notesmodel.user_id == session['user_id'], notesmodel.id.in_(rw_note_data)).order_by(notesmodel.updated_at.desc(),notesmodel.is_pinned.desc()).all()
        form = CreateNoteForm()
        search_form = SearchForm()
        user_labels =  labelmodel.query.filter((labelmodel.is_system_label == True) | (labelmodel.user_id == session['user_id'])).all()
        if notelist:
            return render_template('notes.html',note_list=notelist,notes_message="No Notes To Show",create_form=form,search_form=search_form,label_list = user_labels)
        else:
            return render_template('notes.html',notes_message="No Notes To Show",create_form=form,search_form=search_form,label_list = user_labels)

@blp.route('/manage/labels')
class view_labels(MethodView):

    def get(self):
        try:
            create_form = CreateNoteForm()
            label_form = LabelForm()
            label_list =  labelmodel.query.filter(labelmodel.user_id == session.get('user_id','')).all()
            user_labels =  labelmodel.query.filter((labelmodel.is_system_label == True) | (labelmodel.user_id == session['user_id'])).all()
            return render_template('labels.html', labels = label_list if  label_list else False  ,create_form=create_form,label_list = user_labels,label_form=label_form)
        except Exception as e:
            abort(500,e)
        
@blp.route('/manage/labels/create')
class create_label(MethodView):

    def post(self):
        try:
            form = LabelForm()
            if form.validate_on_submit():
                form_name = form.name.data
                form_user_id = session['user_id']
                new_label = labelmodel(name=form_name,user_id=form_user_id)
                db.session.add(new_label)
                db.session.commit()
                flash('New Label Has Been Created', 'info')
                return redirect(url_for('APP_NOTES.view_labels'))
            else:
                return render_template('labels.html',create_form=form)
        except Exception as e:
            abort(500,e)
        
@blp.route('/manage/labels/delete/<int:label_id>')
class delete_label(MethodView):

    def get(self,label_id):
        try:
            label = labelmodel.query.filter(labelmodel.id == label_id, labelmodel.user_id == session.get('user_id','')).first_or_404()
            db.session.delete(label)
            db.session.commit()
            flash('Label Has Been Deleted Successfully', 'info')
            return redirect(url_for('APP_NOTES.view_labels'))
        except SQLAlchemyError as e:
            abort(500,e)

@blp.route('/manage/labels/modify/<int:label_id>')
class modify_label(MethodView):

    
    def post(self,label_id):
        try:
            form = LabelForm()
            if form.is_submitted():
                form_name = form.name.data
                label = labelmodel.query.filter(labelmodel.id == label_id, labelmodel.user_id == session.get('user_id','')).first_or_404()
                label.name = form_name
                db.session.commit()
                flash('Label Has Been Modified Successfully', 'info')
                return redirect(url_for('APP_NOTES.view_labels'))
            else:
                abort(404)
        except SQLAlchemyError as e:
            abort(500,e)
                

