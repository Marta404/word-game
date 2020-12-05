from flask import Flask, url_for, request, render_template, redirect, jsonify, flash, g, session
# to set up database I'll use SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# to create json from database
from flask_marshmallow import Marshmallow
# to set up an automatic data in the database when creating a new entry
from datetime import datetime


# for login function
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
users.append(Admin(id=1, username='admin@a.com', password='admin'))
users.append(Admin(id=2, username='admin2@a.com', password='admin2'))
users.append(Admin(id=3, username='test@a.com', password='test'))

###############################################################
app = Flask(__name__)
# where the database is located, the database is called test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamedb.db'
# new add secret key
app.config['SECRET_KEY'] = 'THISisMYsecretKey009'


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


        # database
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Todo(db.Model):
    # table for questions
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    week = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return '<Question %r>' % self.id


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo

# for the next Patch
# class Admin(UserMixin, db.Model):
#     # table for admin
#     id = db.Column(db.Integer, primary_key=True)
#     fname = db.Column(db.String(50), nullable=False)
#     sname = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), nullable=False, unique=True)
#     password = db.Column(db.String(50), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # def __repr__(self):
    #     return '<Admin %r>' % self.id

# class AdminSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Admin
##################################################


@app.route('/admin/', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        # remove admin details from the session if credentials incorrect
        session.pop('user_id', None)
        username = request.form['email1']
        password = request.form['pwd']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('account'))

        return redirect(url_for('admin'))

    return render_template('login.html')


@app.route('/account/', methods=['POST', 'GET'])
def account():
    if not g.user:
        return redirect(url_for('admin'))

    return render_template('account.html')


@app.route('/admin/logout/')
def admin_logout():
    session.pop('user_id', None)
    return redirect(url_for('admin'))


@app.route('/admin/add/', methods=['POST', 'GET'])
# add methods POST and GET to handle data flow to and from the database
def admin_add():
    if not g.user:
        return redirect(url_for('admin'))

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
    if not g.user:
        return redirect(url_for('admin'))

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
    if not g.user:
        return redirect(url_for('admin'))

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

############################### GAME ##################################################


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
############################################################################################


@app.errorhandler(404)
# errorhandler - displays a custom error page
def page_not_found(error):
    return "Couldn't find the page you requested.", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
