from flask import render_template, session, redirect, url_for
from . import app_blueprint
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from .search import search


class NameForm(Form):
    keyword = StringField('keyword', validators=[DataRequired()])
    select = SelectField('search in', choices=[('t', 'Title'), ('tc', 'Title & Content')])
    submit = SubmitField('Submit')


links = []


@app_blueprint.route('/', methods=['GET', 'POST'])
def homepage():
    form = NameForm()
    if form.validate_on_submit():
        links.clear()
        links.extend(search(form.keyword.data, form.select.data))
        return redirect(url_for('.homepage'))
    return render_template('index.html', form=form, results=links)
