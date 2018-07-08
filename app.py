from flask import Flask, render_template, url_for, request, redirect, jsonify
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime
from flask_moment import Moment



def connect():
    connection = MongoClient('127.0.0.1', 27017)
    handle = connection["projectfinder"]
    return handle

app = Flask(__name__)
moment = Moment(app)
app.config['ELASTICSEARCH_URL'] = 'http://127.0.0.1:9200/'
es =  Elasticsearch([app.config['ELASTICSEARCH_URL']])
handle = connect()


@app.route('/')
@app.route('/home')
def home():
    projects = handle.itproject.find().sort([("filter_date_post", -1)]).limit(30)
    count = handle.reminders.find().count()
    return render_template('home.html', projects=projects, count=count)

@app.route('/search')
def lookup():
    return render_template('search.html')


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    #results = es.search(index="itproject", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skill_summary"] }}})
    results = handle.itproject.find( { "$text": { "$search": search_term, "$language": "de" } }, { "score": {"$meta": "textScore" } } )
    results.sort([('score', {'$meta': 'textScore'}), ("filter_date_post", -1)]).limit(30)

    #res = es.search(index="itproject", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "category", "type", "link"] }}})
    return render_template('results.html', results=results )

"""@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(index="flask_reminders", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skill_summary"] }}})
    return render_template('results.html', res=res )"""






if __name__ == '__main__':
    app.run(debug=True)
