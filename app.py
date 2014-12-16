import os
import re
import nltk
import operator
from collections import Counter


import requests
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

from stop_words import stops

#################
# configuration #
#################

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *


##########
# routes #
##########

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == 'POST':

        try:

            url = request.form['url']

            if 'http://' not in url[:7] and 'https://' not in url[:8]:
                url = 'http://' + url

            r = requests.get(url)
            print "TEXT: \n", r.text

        except:
            errors.append('Unable to get URL.')
            return render_template('index.html',
                                   errors=errors)

        if r:

            # text processing
            raw = BeautifulSoup(r.text).get_text()
            nltk.data.path.append('./nltk_data/')  # set the path
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)

            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)

            # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            no_stop_words_count = Counter(no_stop_words)

            # save the results
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )
            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count
                )
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")
    return render_template('index.html', errors=errors, results=results)


# fucking delete this
@app.route('/config')
def connnnfig():
    return os.environ['APP_SETTINGS']


print os.environ['APP_SETTINGS']

if __name__ == '__main__':
    app.run()