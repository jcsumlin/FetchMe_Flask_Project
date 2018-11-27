import configparser

from flask import Flask, render_template, flash, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm

config = configparser.ConfigParser()
config.read('auth.ini')
# TODO: Users stored in the database are logged in and session information is stored
# TODO: Management vs Employee Views
# from flaskblog.forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '01a856662e56d9b7eef86549cbfd6bf9c9b2aaf4625e9518'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    is_manager = db.Column(db.Boolean, nullable=False, default=False)
    point_bal = db.Column(db.Integer, nullable=False, default=0)
    driver_rating = db.Column(db.Float(4), nullable=False, default=0.000)
    avg_delivery_time = db.Column(db.Float(3), nullable=False, default=0.00)
    tasks = db.relationship('CompletedTasks', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.full_name}', '{self.is_manager}', '{self.point_bal}')"

class Tasks(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_name = db.Column(db.String(255), nullable=False)
    task_desc = db.Column(db.Text, nullable=False)
    task_point_value = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return(f"Tasks('{self.task_id}', '{self.task_name}'), '{self.task_point_value}'")

class CompletedTasks(db.Model):
    __tablename__ = 'completedtasks'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return(f"CompletedTasks('{self.task_id}', '{self.is_approved}')")

class Bonus(db.Model):
    __tablename__ = 'bonus'
    bonus_id = db.Column(db.Integer, nullable=False, primary_key=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    bonus_name = db.Column(db.String(255), nullable=False)
    bonus_desc = db.Column(db.Text, nullable=False)
    balance_req = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return(f"Bonus('{self.bonus_name}', '{self.is_active}', '{self.balance_req}')")


user = {
    'email': 'jcsumlin@gmail.com',
    'password': 'test',
    'full_name': 'Chat Sumlin',
    'is_mananger': True,
    'point_bal': 10,
    'driver_rating': 4.99,
    'avg_delivery_time': 35.1,
}

def get_user(username: str):
    user = User.query.filter(username=username).all()
    if len(user) == 0:
        return False
    elif len(user) == 1:
        return user[0]
    elif len(user) > 1:
        raise ValueError("Database returned more than one user, this should not be possible")

def get_employees():
    users = User.query.filter(is_manager=False).all()
    return users

def get_tasks():
    pass

def getPoints(id: int):
    pass

def check_password(password, hash):
    if bcrypt.check_password_hash(hash, password):
        return True
    else:
        return False


def create_user(username, password, fullname,driver_rating=0.0, avg_delivery_time=30.0, is_manager=False):
    new_user = User(email=username,
                    password=password,
                    is_manager=is_manager,
                    full_name=fullname,
                    driver_rating=driver_rating,
                    avg_delivery_time=avg_delivery_time)

    try:
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        return [False, e]


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
