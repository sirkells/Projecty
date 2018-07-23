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
    body = {
            "size" : 50,
            "sort": [
            {
              "filter_date_post": {
                "order": "desc"
              }
            },
            "_score"
        ]
    }
    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:200],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['location'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=False)
    #res = es.search(index="projectfinder", body=body)
    return render_template('home.html', res=projects, now=datetime.utcnow())

@app.route('/home/search')
@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    body = {
            "size" : 50,
            "query": {
              "multi_match": {
                "query": search_term,
                "fields": ["description", "title", "skills.keywords^2", "category"],
                "fuzziness" : "AUTO",
                "prefix_length" : 2
              }
            }
          }
    result = es.search(
        index='projectfinder',
        body=body
        )
    try:
        # clean up
        docs = [{
            'source': doc['_source'],
            'score': doc['_score'],
            'id': doc['_id']
        } for doc in result['hits']['hits']]
    except KeyError:
        # return message
        return render_template('noresult.html')

    projects = [{
        'id': hit['id'],
        'title': hit['source']['title'],
        'description': hit['source']['description'][:600],
        'filter_date_post': datetime.strptime(hit['source']['filter_date_post'], '%Y-%m-%dT%H:%M:%S') if hit['source']['filter_date_post'] else datetime.utcnow(),
        #'cockpit': True if hit['id'] in cockpit_set else False,
        'url': hit['source']['url'],
        'count': hit['source']['person_count'],
        'duration': hit['source']['duration'],
        'location': hit['source']['location'],
        'source': hit['source']['source'],
        'score': '{:.2f}'.format(hit['score'])
                } for hit in docs]
    projects = sorted(projects, key=lambda p: p['filter_date_post'], reverse=True)

    count = result['hits']['total']
    return render_template('results.html', res=projects, search_term=search_term, count=count, now=datetime.utcnow())


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
