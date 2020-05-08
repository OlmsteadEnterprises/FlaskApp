from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '97f9d4c872b34c19f7b004b8744346ff3a01c7ab0850a8017693a792214b3363'

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route('/about')
def about():
    return render_template("about.html", title='About')

if __name__ == '__main__':
    app.run(debug=True)
