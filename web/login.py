from flask import Flask


login = Flask(__name__)


@login.route('/')
def hello():
    return "hello"



if __name__ == '__main__':
    login.run(host="0.0.0.0", debug=True)