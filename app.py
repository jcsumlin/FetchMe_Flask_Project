from flask import Flask, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt

from forms import LoginForm
import pymysql.cursors
import configparser
config = configparser.ConfigParser()
config.read('auth.ini')

# from flaskblog.forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '01a856662e56d9b7eef86549cbfd6bf9c9b2aaf4625e9518'





def get_user(username):
    connection = pymysql.connect(host='fetchme.cg1iufnmopx8.us-west-2.rds.amazonaws.com',
                                 port=3306,
                                 user=config.get('auth', 'mysql_user'),
                                 password=config.get('auth', 'mysql_password'),
                                 db='fetchme',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `password` FROM `users` WHERE `username`=%s"
            cursor.execute(sql, (username))
            result = cursor.fetchone()
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()
    return result


def check_password(password, hash):
    if bcrypt.check_password_hash(hash, password):
        return True
    else:
        return False


def create_user(username, password, is_manager=0):
    connection = pymysql.connect(host='fetchme.cg1iufnmopx8.us-west-2.rds.amazonaws.com',
                                 port=3306,
                                 user=config.get('auth', 'mysql_user'),
                                 password=config.get('auth', 'mysql_password'),
                                 db='fetchme',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `users` (`username`, `password`, `is_manager`) VALUES (%s, %s, %s)"
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute(sql, (username, password, is_manager))

        connection.commit()
    except Exception as e:
        print(e)
        return False

    finally:
        connection.close()
    return "user %s has been created" % username


bcrypt = Bcrypt(app)
# hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')
# bcrypt.check_password_hash(hashed_pw, 'password') # returns False
# bcrypt.check_password_hash(hashed_pw, 'testing') # returns True
site_title = "| FetchMe Points Program"
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return login()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        hashed_pw = get_user(form.username.data)['password']
        if get_user(form.username.data) != False and check_password(form.password.data, hashed_pw) == True:
            flash(f"You have been logged in! {form.username.data}", category="success")
            return redirect(url_for('dashboard'))
        else:
            flash("Your username and password did not match!", category='danger')
    return render_template('login.html', name="Login Page {0}".format(site_title), form=form)

@app.route('/dashboard')
def dashboard():
    return "You're in!"

if __name__ == '__main__':
    app.run(debug=True)
