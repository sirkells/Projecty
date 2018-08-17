from flask import Flask, render_template, url_for, request, redirect, jsonify, abort, flash
from pymongo import MongoClient
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from datetime import datetime
from flask_moment import Moment


app = Flask(__name__)
moment = Moment(app)
app.config['SECRET_KEY'] = 'password'
app.config['ELASTICSEARCH_URL'] = 'http://127.0.0.1:9200/'
es =  Elasticsearch([app.config['ELASTICSEARCH_URL']])
client = Elasticsearch()


@app.route('/dsl')
def dsl():
    s = Search(using=client, index="projectfinder") \
        .query("match", skills="python")

    s.aggs.bucket('Location', 'terms', field='region.keyword')

    response = s.execute()
    print(len(response))

    for hit in response:
        print(hit.location, hit.title)

    for tag in response.aggregations.Location.buckets:
        print(tag.key, tag.doc_count)

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)