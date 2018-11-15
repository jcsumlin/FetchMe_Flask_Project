import configparser

import pymysql.cursors
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_bcrypt import Bcrypt

from forms import LoginForm

config = configparser.ConfigParser()
config.read('auth.ini')
# TODO: Users stored in the database are logged in and session information is stored
# TODO: Management vs Employee Views
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
            sql = "SELECT * FROM `users` WHERE `username`=%s"
            cursor.execute(sql, (username))
            result = cursor.fetchone()
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()
    return result

def get_employees():
    connection = pymysql.connect(host='fetchme.cg1iufnmopx8.us-west-2.rds.amazonaws.com',
                                 port=3306,
                                 user=config.get('auth', 'mysql_user'),
                                 password=config.get('auth', 'mysql_password'),
                                 db='fetchme',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `users`"
            cursor.execute(sql)
            result = cursor.fetchone()
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()
        return result

def get_tasks():
    pass

def getPoints(id: int):
    connection = pymysql.connect(host='fetchme.cg1iufnmopx8.us-west-2.rds.amazonaws.com',
                                 port=3306,
                                 user=config.get('auth', 'mysql_user'),
                                 password=config.get('auth', 'mysql_password'),
                                 db='fetchme',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT users.full_name, tasks.task_name, user_points.approved FROM fetchme.users, fetchme.tasks, fetchme.user_points WHERE (user_points.user_id={id} AND users.id={id} AND user_points.approved=2)".format(id=id)
            cursor.execute(sql, (id))
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
hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')
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
        if get_user(form.username.data) != None:
            user = get_user(form.username.data)
            hashed_pw = user['password']
            if get_user(form.username.data) != False \
                    and check_password(form.password.data, hashed_pw) == True:
                flash(f"You have been logged in! {form.username.data}", category="success")
                session['logged_in'] = True
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_manager'] = user['is_manager']
                session['point_balance'] = user['point_balance']
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid ID or password. Please try again.", category='danger')
        else:
            flash("Invalid ID or password. Please try again.", category='danger')
    return render_template('login.html', name="Login Page {0}".format(site_title), form=form)


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash("You must be logged in to view that page.",
              category='danger')
        return redirect('/login')
    else:
        if ord(session['is_manager']) == 1:
            if 'points_approved' in session:
                data_1 = session['points_approved']
            else:
                data_1 = "Error"
            if 'points_pending' in session:
                data_2 = session['points_pending']
            else:
                data_2 = "Error"
            if 'points_approved' in session:
                data_3= session['points_approved']
            else:
                data_3 = "Error"
            return render_template('dashboard_admin.html',
                                   name="Dashboard {0}".format(site_title),
                                   data_1=data_1,
                                   data_2=data_2,
                                   data_3=data_3,
                                   points=getPoints(session['user_id']))
        else:
            return render_template('dashboard_user.html',
                                   name="Dashboard {0}".format(site_title))


@app.route("/reports")
def report_page():
    if session['is_manager'] is False:
        flash("Error 403: Forbidden", category="danger")
        return redirect('/dashboard')
    else:
        return render_template("reports.html")


@app.route("/task-details")
def task_review(task):
    if session['is_manager'] is True:
        return render_template('task_review_manager.html', task=task)
    else:
        return render_template('task_review_driver.html', task=task)

@app.route("/account")
def account():
    return render_template('account.html', account=get_current_user())

@app.route("/bonus")
def bonus():
    return render_template("bonus_table.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/login')

@app.route("/submit-points")
def submit_points():
    return render_template("submit_points.html", tasks = get_tasks())

@app.route("/employee-management")
def employee_management():
    return render_template("employee_management.html", employees = get_employees())

@app.route("/task-management")
def task_management():
    return render_template("task_management.html", tasks = get_tasks())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', name="Error 404 {0}".format(site_title)), 404


if __name__ == '__main__':
    app.run()
