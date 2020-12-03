from flask import Flask, url_for, request, render_template, redirect, jsonify
# to set up database I'll use SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# to create json from database
from flask_marshmallow import Marshmallow
# to set up an automatic data in the database when creating a new entry
from datetime import datetime

app = Flask(__name__)
# where the database is located, the database is called test.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Todo(db.Model):
    # table for questions
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    week = db.Column(db.String(5), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class Admin(db.Model):
    # table for admin
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    sname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    #password = db.Column(db.String(100), nullable=False)
    # to retrieve what has been created; to get from the database the question and it's id

    def __repr__(self):
        return '<Question %r>' % self.id


class QuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo


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


@app.route('/admin/', methods=['POST', 'GET'])
# for testing admin panel navigation - temporary directory
def admin(name=None):
    # return render_template('login.html')
    if request.method == 'POST':
        # print(request.form)
        name = request.form['email1']
        # templates word-game.html + admin.html body content
        # return render_template('login.html')
        # return render_template('account.html', name=name)
        return redirect('/admin/account/', name=name)
    else:
        return render_template('login.html')


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


@app.route('/admin/account/')
def admin_account():
    # templates word-game.html + edit.questions.html body content
    return render_template('account.html')


@app.errorhandler(404)
# errorhandler - displays a custom error page
def page_not_found(error):
    return "Couldn't find the page you requested.", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
