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
    page_size = 100
    project = handle.itproject.find().limit(page_size)
    projects = sorted(project, key=lambda p: p['filter_date_post'], reverse=True)
    count = handle.itproject.find().count()
    return render_template('home.html', projects=projects, count=count)
    """def home():
        projects = handle.itproject.find().sort([("filter_date_post", -1)].limit(150)
        count = handle.itproject.find().count()
        return render_template('home.html', projects=projects, count=count)"""


@app.route('/pagination/')
def pagination():
    numberr = handle.itproject
    offset = int(handle.itproject.find().count()) - 1 #getting the oldest project number by filter_date_post in collection
    count = handle.itproject.find().count() #total number of project in collection
    #offset = int(off) - 1
    start_id = numberr.find().sort('_id', -1)
    last_id = start_id[offset]['_id'] #oldest project id in collection. this would be used to sort by id since id is created by time added
    limit = 20
    numbery = numberr.find({'_id' : {'$gte' : last_id}}).sort('_id', -1).limit(limit) #sorts the project by the most recent first
    output = []
    for i in numbery:
        output.append({'title': i['title']})
    next_url = '/numbery?limit=' + str(limit) + '&offset=' + str(offset + limit)
    prev_url = '/numbery?limit=' + str(limit) + '&offset=' + str(offset - limit)
    return jsonify({'result' : output, 'next_url': next_url, 'prev_url': prev_url, 'count': count })

"""@app.route('/pagination')
def pagination():
    numberr = handle.numbers
    offset = int(handle.numbers.find().count()) - 1
    count = handle.numbers.find().count()
    #offset = int(off) - 1
    start_id = numberr.find().sort('_id', -1)
    last_id = start_id[offset]['_id']
    limit = 20
    numbery = numberr.find({'_id' : {'$gte' : last_id}}).sort('_id', -1).limit(limit)
    output = []
    for i in numbery:
        output.append({'title': i['number']})
    return jsonify({'result' : output, 'next_url': '', 'prev_url': '', 'count': count })"""



@app.route('/search')
def lookup():
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
    count = results.count()

    #res = es.search(index="itproject", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "category", "type", "link"] }}})
    return render_template('results.html', results=results, search_term=search_term, count=count)

"""@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]
    res = es.search(index="flask_reminders", size=20, body={"query": {"multi_match" : { "query": search_term, "fields": ["description", "title", "skill_summary"] }}})
    return render_template('results.html', res=res )"""






if __name__ == '__main__':
    app.run(debug=True)
