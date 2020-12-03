from flask import Flask, url_for, request, render_template, redirect, jsonify, flash
# to set up database I'll use SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# to create json from database
from flask_marshmallow import Marshmallow
# to set up an automatic data in the database when creating a new entry
from datetime import datetime
# new to use login
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
# where the database is located, the database is called test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamedb.db'
# new add secret key
app.config['SECRET_KEY'] = 'THISisMYsecretKey009'
db = SQLAlchemy(app)
ma = Marshmallow(app)
# new to login
login_manager = LoginManager()
# login_manager.init.app(app)
# new to login, userMix will enable a few additional methods

######################################################################


class Todo(db.Model):
    # table for questions
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    week = db.Column(db.String(5), nullable=False)


class Admin(UserMixin, db.Model):
    # table for admin
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    sname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Question %r>' % self.id
    # to retrieve what has been created; to get from the database the question and it's id


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo

# new user login


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))


@app.route('/admin/')
def admin():
    return render_template('login.html')


@app.route('/admin/', methods=['POST'])
# for testing admin panel navigation - temporary directory
def admin_post():
    email = request.form.get('email1')
    password = request.form.get('pwd')

    admin = Admin.query.filter_by(email=email).first()

    if not admin and not check_password_hash(admin.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('admin'))

    login_user(admin)

    return redirect(url_for('admin/account'))


@app.route('/admin/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/admin/')


@app.route('/admin/account/')
@login_required
def admin_account():
    admin = current_user.fname + " " + current_user.sname
    return render_template('account.html', admin_name=admin)
    ##############################################################


@app.route('/', methods=['GET', 'POST'])
def root():
    # templates word-game.html + newgame.html body content
    return render_template('newgame.html')


@app.route('/api/')
def api():
    questions = Todo.query.order_by(Todo.week).all()
    #questions = Todo.query.all()
    question_schema = QuestionSchema(many=True)
    output = question_schema.dump(questions)
    return jsonify({'questions': output})


# @app.route('/admin/', methods=['POST', 'GET'])
# # for testing admin panel navigation - temporary directory
# def admin(name=None):
#     # return render_template('login.html')
#     if request.method == 'POST':
#         # print(request.form)
#         email = request.form['email1']
#         name = {name: email}
#         return redirect('/admin/account/')
#     else:
#         return render_template('login.html')


# @app.route('/admin/account/')
# def admin_account():
#     # templates word-game.html + edit.questions.html body content
#     return render_template('account.html')


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
