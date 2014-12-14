from flask import Flask
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    return "Hello Muthafucka!"


@app.route('/<name>')
def hello_name(name):
    return "Hello, {}".format(name)


@app.route('/config')
def connnnfig():
    return os.environ['APP_SETTINGS']


print os.environ['APP_SETTINGS']

if __name__ == '__main__':
    app.run()