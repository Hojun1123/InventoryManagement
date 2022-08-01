from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('LOGIN.html')

@app.route('/main')
def main():
    return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(debug=True)