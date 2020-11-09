from flask import Flask, url_for, request, render_template
app = Flask(__name__)


@app.route('/')
def root():
    # templates word-game.html + newgame.html body content
    return render_template('newgame.html')


@app.route('/admin/')
# for testing admin panel navigation - temporary directory
# @app.route('/admin/<name>')
def admin(name=None):
    # templates word-game.html + admin.html body content
    return render_template('admin.html')


# in test mode - admin panel directories - no credentials required yet
@app.route('/admin/add/')
def admin_add(name=None):
    # templates word-game.html + add.questions.html body content
    return render_template('add.question.html')


# in test mode - admin panel directories - no credentials required yet
@app.route('/admin/edit/')
def admin_edit(name=None):
    # templates word-game.html + edit.questions.html body content
    return render_template('edit.questions.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
