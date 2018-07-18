from flask import Flask, render_template, url_for, request, redirect, jsonify, abort, flash
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
    page_size = 30
    project = handle.itproject.find().limit(page_size)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    count = handle.itproject.find().count()
    
    """doc = {
            "size" : 50,
            "sort": [
                {
                    "filter_date_post" : {"order" : "desc"}
                }
            ]
          }
    res = es.search(index="projectfinder", body=doc)
    return render_template('home.html', res=res, now=datetime.utcnow())"""
    return render_template('home.html', projects=projects, count=count)
    """def home():
        projects = handle.itproject.find().sort([("filter_date_post", -1)].limit(150)
        count = handle.itproject.find().count()
        return render_template('home.html', projects=projects, count=count)"""

@app.route('/home/search')
@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    #results = es.search(index="itproject", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skill_summary"] }}})
    results = handle.itproject.find( { "$text": { "$search": search_term, "$language": "de" } }, { "score": {"$meta": "textScore" } } )
    results.sort([('score', {'$meta': 'textScore'}), ("filter_date_post", -1)]).limit(30)
    #results.sort([('score', {'$meta': 'textScore'}), ("filter_date_post", 1)]).limit(30)
    #{ date: 1, score: { $meta: "textScore" } }
    #results.sort('score', {'$meta': 'textScore'}, 'datefiel', -1).limit(100)
    result = es.search(index="projectfinder", body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skills", "category"] }}})
    count = result['hits']['total']
    """for hit in result['hits']['hits']:

    docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if result['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['location'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } ]"""
    doc = {
            "size" : 50,
            "query": {
              "multi_match": {
                "query": search_term,
                "fields": ["description", "title", "skills", "category"]
              }
            }
          }

    res = es.search(index="projectfinder", body=doc)
    return render_template('results.html', res=res, search_term=search_term, count=count, now=datetime.utcnow())

"""@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(index="flask_reminders", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skill_summary"] }}})
    return render_template('results.html', res=res )"""






if __name__ == '__main__':
    app.run(debug=True)


"""
 for hit in result['hits']['hits']:


    docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if result['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['location'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } ]
    doc = {
            "size" : 50,
            "query": {
              "multi_match": {
                "query": search_term,
                "fields": ["description", "title", "skills", "category"]
              }
            }
          }"""

    #res = es.search(index="projectfinder", body=doc)

    """@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(index="flask_reminders", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skill_summary"] }}})
    return render_template('results.html', res=res )"""

#results = es.search(index="itproject", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skill_summary"] }}})
    #results = handle.itproject.find( { "$text": { "$search": search_term, "$language": "de" } }, { "score": {"$meta": "textScore" } } )
    #results.sort([('score', {'$meta': 'textScore'}), ("filter_date_post", -1)]).limit(30)
    #results.sort([('score', {'$meta': 'textScore'}), ("filter_date_post", 1)]).limit(30)
    #{ date: 1, score: { $meta: "textScore" } }
    #results.sort('score', {'$meta': 'textScore'}, 'datefiel', -1).limit(100)
    #result = es.search(index="projectfinder", body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skills", "category"] }}})
    #count = result['hits']['total']

    #return render_template('home.html', projects=projects, count=count)
    """def home():
        projects = handle.itproject.find().sort([("filter_date_post", -1)].limit(150)
        count = handle.itproject.find().count()
        return render_template('home.html', projects=projects, count=count)"""

#page_size = 30
    #project = handle.itproject.find().limit(page_size)
    #projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    #count = handle.itproject.find().count()