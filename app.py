import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

@app.route('/')
def hello():
    return "Hello Muthafucka!"


@app.route('/<name>')
def hello_name(name):
    return "Hello, {}".format(name)


# fucking delete this
@app.route('/config')
def connnnfig():
    return os.environ['APP_SETTINGS']


print os.environ['APP_SETTINGS']

if __name__ == '__main__':
    app.run()