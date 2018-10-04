from flask import Flask, render_template,flash,redirect,url_for
from flask_bcrypt import Bcrypt
from forms import LoginForm
# from flaskblog.forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '01a856662e56d9b7eef86549cbfd6bf9c9b2aaf4625e9518'
bcrypt = Bcrypt(app)
hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')
bcrypt.check_password_hash(hashed_pw, 'password') # returns False
bcrypt.check_password_hash(hashed_pw, 'testing') # returns True
site_title = "| FetchMe Points Program"
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return login()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"You have been logged in! {form.username.data}", category="success")
        return redirect(url_for('dashboard'))
    return render_template('login.html', name="Login Page {0}".format(site_title), form=form)

@app.route('/dashboard')
def dashboard():
    return "You're in!"

if __name__ == '__main__':
    app.run(debug=True)
