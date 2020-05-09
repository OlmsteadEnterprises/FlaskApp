from FlaskApp import Flask, app, render_template, redirect, flash, url_for, request
from FlaskApp.forms import RegistrationForm, LoginForm
from FlaskApp import db, bcrypt
from FlaskApp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author':'Travis Olmstead',
        'title':'Blog Post 1',
        'content':'First Post',
        'date_posted':'May 5, 2020'
    },
    {
        'author':'Travis Olmstead',
        'title':'Blog Post 1',
        'content':'First Post',
        'date_posted':'May 5, 2020'
    }
]

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html", posts=posts)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in!', 'success')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created!  You may now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in!', 'success')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Successful Login!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful!  Please check email and password!', 'danger')
    return render_template("login.html", form=form, title='Login')

@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have been logged out!', 'danger')
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template("account.html", title='Account')

@app.route('/about')
def about():
    return render_template("about.html", title='About')
