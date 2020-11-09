from flask import Flask, url_for, request, render_template
app = Flask(__name__)


@app.route('/')
# for testing admin panel navigation - temporary directory
@app.route('/<name>')
def root(name=None):
    # templates word-game.html + newgame.html
    return render_template('newgame.html')


@app.route('/admin/')
def admin():
    return render_template('admin.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
