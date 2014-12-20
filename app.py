import os
import re
import nltk
import operator
from collections import Counter

import requests
from rq import Queue
from rq.job import Job
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

from stop_words import stops
from worker import conn

#################
# configuration #
#################

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

q = Queue(connection=conn)

from models import *

##########
# helper #
##########


def count_and_save_words(url):
    errors = []

    try:
        r = requests.get(url)

    except:
        errors.append("Unable to get URL. Please make sure it's valid and try again")

        return {"error": errors}

    # text processing
    raw = BeautifulSoup(r.text).get_text()
    nltk.data.path.append


##########
# routes #
##########

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == 'POST':

        url = request.form['url']

        if 'http://' not in url[:7] or 'https://' not in url[:8]:
            url = 'http://' + url

        job = q.enqueue_call(
            func=count_and_save_words, args=(url,), result_ttl=5000
        )
        print job.get_id()

    return render_template('index.html', results=results)


# fucking delete this
@app.route('/config')
def connnnfig():
    return os.environ['APP_SETTINGS']


print os.environ['APP_SETTINGS']

if __name__ == '__main__':
    app.run()