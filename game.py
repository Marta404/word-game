# from workbook
import bcrypt
from functools import wraps
from flask import Flask
#################################################################
from flask import Flask, url_for, request, render_template, redirect, jsonify, flash, session
# to set up database I'll use SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# to create json from database
from flask_marshmallow import Marshmallow
# to set up an automatic data in the database when creating a new entry
from datetime import datetime
# new to use login
# , login_user, login_required, logout_user, current_user
from flask_login import LoginManager, UserMixin
##from werkzeug.security import generate_password_hash, check_password_hash


class Admin:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        # to check if it works:

    def __repr__(self):
        return f'<Admin: {self.username}>'


# global variable for all the admins:
users = []
users.append(Admin(id=1, username='admin@a.com', passwoerd='admin'))


###############################################################
app = Flask(__name__)
# where the database is located, the database is called test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamedb.db'
# new add secret key
app.config['SECRET_KEY'] = 'THISisMYsecretKey009'
db = SQLAlchemy(app)
ma = Marshmallow(app)
# new to login
###login_manager = LoginManager()
# login_manager.init.app(app)
# new to login, userMix will enable a few additional methods
######################################################################
# app.secret_key = 'THISisMYsecretKey009'
# valid_email = 'admin@a.com'
# valid_pwhash = bcrypt.hashpw('secretpass'.encode('utf-8'), bcrypt.gensalt())


class Todo(db.Model):
    # table for questions
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    week = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return '<Question %r>' % self.id


# class Admin(UserMixin, db.Model):
#     # table for admin
#     id = db.Column(db.Integer, primary_key=True)
#     fname = db.Column(db.String(50), nullable=False)
#     sname = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), nullable=False, unique=True)
#     password = db.Column(db.String(50), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # to retrieve what has been created; to get from the database the question and it's id

    # def __repr__(self):
    #     return '<Admin %r>' % self.id


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo


# class AdminSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Admin

##################################################
# create a global variable for an admin


@app.route('/admin/', methods=['POST', 'GET'])
def admin():
    return render_template('login.html')


@app.route('/account/', methods=['POST', 'GET'])
def account():
    return render_template('account.html')


@app.route('/admin/logout/')
def admin_logout():
    return redirect(url_for('admin'))


#########################################################################################################
# def check_auth(email, password):
#     if (email == valid_email and valid_pwhash == bcrypt.hashpw(password.encode('utf-8'), valid_pwhash)):
#         return True
#     return False


# def requires_login(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         status = session.get('logged_in', False)
#         if not status:
#             return redirect('/admin/')
#         return f(*args, **kwargs)
#     return decorated


# @app.route('/admin/logout/')
# def admin_logout():
#     session['logged_in'] = False
#     return redirect(url_for('admin'))


# @app.route('/account/', methods=['POST', 'GET'])
# # @requires_login
# def account():
#     admins = Admin.query.order_by(Admin.id).all()
#     # templates word-game.html + add.questions.html body content
#     return render_template('account.html', admins=admins)
#     # return render_template('account.html')


# @app.route('/admin/', methods=['POST', 'GET'])
# def admin():
#     if request.method == 'POST':
#         user = request.form['email1']
#         pw = request.form['pwd']

#         if check_auth(user, pw):
#             session['logged_in'] = True
#             return 'logged'
#     return render_template('login.html')

    ######################################################################


@app.route('/', methods=['GET', 'POST'])
def root():
    # templates word-game.html + newgame.html body content
    return render_template('newgame.html')


@app.route('/api/')
def api():
    questions = Todo.query.order_by(Todo.week).all()
    question_schema = QuestionSchema(many=True)
    output = question_schema.dump(questions)
    return jsonify({'questions': output})


# in test mode - admin panel directories - no credentials required yet
@app.route('/admin/add/', methods=['POST', 'GET'])
# add methods POST and GET to handle data flow to and from the database
def admin_add():
    if request.method == 'POST':
        # get what is in input field called question and sent to the db
        task_question = request.form['question']
        task_answer = request.form['answer']
        task_week = request.form['weeks']
        # create Todo object
        new_task = Todo(question=task_question,
                        answer=task_answer, week=task_week)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/admin/add/')
        except:
            return 'There was an issue adding your question'

    else:
        # render all the questions which are currently in the db ---> pierwszy == .first()
        questions = Todo.query.order_by(Todo.week).all()
        # templates word-game.html + add.questions.html body content
        return render_template('add.question.html', questions=questions)


@app.route('/admin/delete/<int:id>')
# to delete a question from the list/db
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return render_template('deleted.html')
    except:
        return 'There was a problem deleting that task'

# in test mode - admin panel directories - no credentials required yet


@app.route('/admin/edit/<int:id>', methods=['POST', 'GET'])
def admin_edit(id):
    question = Todo.query.get_or_404(id)

    if request.method == 'POST':
        # update logic
        question.question = request.form['question']
        question.answer = request.form['answer']
        question.week = request.form['weeks']
        try:
            db.session.commit()
            return redirect('/admin/add/')
        except:
            return 'There was an issue with updating the task'

    else:
        return render_template('edit.questions.html', question=question)


@app.errorhandler(404)
# errorhandler - displays a custom error page
def page_not_found(error):
    return "Couldn't find the page you requested.", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
