from flask import Blueprint
from flask import Flask, Response, render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from homepage import db
from homepage.notes.forms import NewNoteForm
from homepage.models import User, Note

notes = Blueprint('notes', __name__)

@notes.route('/new_note', methods=['GET', 'POST'])
@login_required
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("main.home"))
    return render_template("new_note.html", title="New Note", form=form)

@login_required
@notes.route('/notes')
def view_notes():
    return(render_template('notes.html', notes=current_user.notes))

@login_required
@notes.route("/notes/<int:note_id>", methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if current_user.id != note.user_id:
        abort(403)
    form = NewNoteForm()
    if form.validate_on_submit():
        note.content = form.content.data
        note.title = form.title.data
        db.session.commit()
        flash("Your Note has been Updated", "success")
        return redirect(url_for('notes.view_notes'))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('edit_note.html', title=note.title, note=note, form=form)

@login_required
@notes.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if current_user.id != note.user_id:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Your Note has been deleted!', 'info')
    return redirect(url_for('main.home'))

