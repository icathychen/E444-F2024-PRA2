from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired, Email, StopValidation, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

class CustomEmail(Email):
    def __init__(self, message=None):
        if not message:
            message = "Invalid email."
        super(CustomEmail, self).__init__(message=message)

    def __call__(self, form, field):
        if '@' not in field.data:
            message = ("Please include an \'@\' in the email address. \'%s\' is missing an \'@\'.") % field.data
            raise ValidationError(message=message)
        super(CustomEmail, self).__call__(message=message)


def validate_email(form, field):
        if '@' not in (field.data):
            field.errors[:] = []
            message = field.gettext('Please include an \'@\' in the email address. \'%s\' is missing an \'@\'.') % field.data
            raise ValidationError(message)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email address?', validators=[DataRequired(), CustomEmail()])
    submit = SubmitField('Submit')
    
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!') 
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!') 
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html',form = form, name = session.get('name'), email=session.get('email'))

