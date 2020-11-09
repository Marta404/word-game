from flask import Flask, url_for, request, render_template
app = Flask(__name__)


@app.route('/')
def root():
    return render_template('word-game.html')


@app.route('/admin/')
def admin():
    return render_template('admin.html')

 if __name__ == "__main__":
     app.run(host='0.0.0.0', debug=True)
