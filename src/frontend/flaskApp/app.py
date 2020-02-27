import json
import sys
sys.path.append('src/database/classes')
sys.path.append('src/utils')
from NeoReddit import NeoReddit 
from Configuration import Configuration
from flask import render_template, flash, request, redirect
from flask_caching import Cache
from flask import Flask


config = {
        "DEBUG": False,
        "CACHE_TYPE": "simple",
        "CACHE_DAFAULT_TIMEOUT": 300
}

app  = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

cfg = Configuration.configuration('config.yml')
neoReddit = NeoReddit(cfg)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['text']
        return search_results(name)

    return render_template('home.html')


def authorToAuthors(name):

    authorRecords = neoReddit.authorToAuthors(name, 5)

    if not authorRecords:
        return None, None, None

    karma = neoReddit.getKarma(name)
    subList = neoReddit.authorToSubs(name, 5)
    selfSubs = []
    for record in subList:
        val = 100*record[1]/karma
        if val >= 1:
            string = '%s %d%%' % (record[0], round(val))
        else:
            string = '%s %.2g%%' % (record[0], val)

        selfSubs.append(string) 
    

    authors = []
    subInfo = []
    for record in authorRecords:
        authorName = record[0]
        authorKarma = neoReddit.getKarma(authorName)
        string = ''
        authorSubs = neoReddit.authorToSubs(authorName, 3)
        for subRecord in authorSubs:
            # Show whole percentage if above 1, otherwise 
            # show two significant digits
            val = 100*subRecord[1]/authorKarma
            if val >= 1:
                string += '%s %d%%, ' % (subRecord[0], round(val))
            else:
                string += '%s %.2g%%, ' % (subRecord[0], val)
            
        authors.append(authorName)
        subInfo.append(string[:-2])

    return selfSubs, authors, subInfo

@app.route('/results', methods=['GET', 'POST'])
def search_results(name):
    print(name) 
    selfSubs, authors, subInfo = authorToAuthors(name) 

    if selfSubs == None:
        return render_template('error.html' )

    return render_template('results.html',  name = name, \
                                            len=len(authors), \
                                            subs = selfSubs, \
                                            authors = authors, \
                                            otherSubs = subInfo)

if __name__ == "__main__":
    app.run('0.0.0.0', 80)
