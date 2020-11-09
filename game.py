from flask import Flask, url_for, request, render_template
app = Flask(__name__)


@app.route('/')
def root():
    # templates word-game.html + newgame.html body content
    return render_template('newgame.html')


@app.route('/admin/', methods=['POST', 'GET'])
# for testing admin panel navigation - temporary directory
def admin():
    if request.method == 'POST':
        print(request.form)
        name = request.form['email1']
        # templates word-game.html + admin.html body content
        return render_template('login.html')
    else:
        return render_template('login.html')


# in test mode - admin panel directories - no credentials required yet
@app.route('/admin/add/')
def admin_add():
    # templates word-game.html + add.questions.html body content
    return render_template('add.question.html')


# in test mode - admin panel directories - no credentials required yet
@app.route('/admin/edit/')
def admin_edit():
    # templates word-game.html + edit.questions.html body content
    return render_template('edit.questions.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
